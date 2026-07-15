from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from app.schemas.interaction import InteractionResponse


class ChatMessage(BaseModel):
    id: UUID
    role: str
    content: str
    timestamp: datetime


class ChatRequest(BaseModel):
    message: str
    interactionId: UUID | None = None


class ChatResponse(BaseModel):
    message: ChatMessage
    interaction: InteractionResponse | None = None
    metadata: dict | None = None