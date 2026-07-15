import pytz
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from app.db.session import getDb
from app.agents.graph import graph
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatMessage
)

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
        payload: ChatRequest,
        db: Session = Depends(getDb)
):
    initialState = {
        "userMessage": payload.message,
        "currentInteraction": None,
        "selectedTool": None,
        "toolResult": None,
        "assistantResponse": None,
        "db": db,
        "interactionId": payload.interactionId,
    }

    result = graph.invoke(initialState)

    toolResult = result.get(
        "toolResult"
    )

    assistantMessage = ChatMessage(
        id=uuid4(),
        role="assistant",
        content=result["assistantResponse"],
        timestamp=datetime.now(
            pytz.timezone("Asia/Kolkata")
        )
    )

    if isinstance(toolResult, dict):
        interaction = toolResult.get("interaction")
        metadata = toolResult.get("metadata")
    else:
        interaction = toolResult
        metadata = None

    return ChatResponse(
        message=assistantMessage,
        interaction=interaction,
        metadata=metadata,
    )
