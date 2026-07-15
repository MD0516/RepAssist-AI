from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import getDb
from app.services.interactionService import (
    getAllInteractions,
    getInteractionById,
)

router = APIRouter(
    prefix="/interactions",
    tags=["Interactions"]
)

@router.get("/")
def getInteractions(
    db: Session = Depends(getDb)
):
    interactions = getAllInteractions(
        db
    )

    return interactions

@router.get("/{interactionId}")
def getInteraction(
    interactionId: UUID,
    db: Session = Depends(getDb)
):
    interaction = getInteractionById(
        db,
        interactionId
    )

    if not interaction:
        raise HTTPException(
            status_code=404,
            detail="Interaction not found"
        )

    return interaction