from sqlalchemy.orm import Session

from app.models.interaction import Interaction
from app.schemas.interaction import InteractionFilters


def createInteraction(
        db: Session,
        interactionData: dict
):
    interaction = Interaction(
        **interactionData
    )

    db.add(interaction)

    db.commit()

    db.refresh(interaction)

    return interaction


def getInteractionById(
        db: Session,
        interactionId
):
    return (
        db.query(Interaction)
        .filter(
            interactionId == Interaction.id
        )
        .first()
    )


def updateInteraction(
        db: Session,
        interaction,
        updates: dict,
):
    for field, value in updates.items():
        setattr(
            interaction,
            field,
            value,
        )

    db.commit()

    db.refresh(
        interaction
    )

    return interaction


def getAllInteractions(db: Session):
    return (
        db.query(Interaction)
        .order_by(
            Interaction.createdAt.desc()
        )
        .all()
    )


def getInteractionsByHcp(
        db: Session,
        hcpName: str,
):
    return (
        db.query(Interaction)
        .filter(
            hcpName == Interaction.hcpName
        )
        .all()
    )


from datetime import datetime, timedelta


def filterInteractions(
        db: Session,
        filters: InteractionFilters,
):
    query = db.query(Interaction)

    if filters.hcpName:
        query = query.filter(
            Interaction.hcpName.ilike(f"%{filters.hcpName}%")
        )

    if filters.productDiscussed:
        query = query.filter(
            Interaction.productDiscussed.ilike(f"%{filters.productDiscussed}%")
        )

    if filters.sentiment:
        query = query.filter(
            filters.sentiment == Interaction.sentiment
        )

    if filters.interactionType:
        query = query.filter(
            filters.interactionType == Interaction.interactionType
        )

    if filters.lookbackDays:
        cutoff = datetime.now() - timedelta(days=filters.lookbackDays)
        query = query.filter(
            Interaction.interactionDate >= cutoff
        )

    return query.all()
