from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    JSON, ARRAY
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    hcpName = Column(String, nullable=True)

    interactionDate = Column(DateTime, nullable=True)

    interactionType = Column(String, nullable=True)

    productDiscussed = Column(String, nullable=True)

    sentiment = Column(String, nullable=True)

    materialsShared = Column(
        JSON,
        default=list
    )

    keyDiscussionPoints = Column(
        Text,
        nullable=True
    )

    followUpRequired = Column(
        Boolean,
        default=False
    )

    followUpNotes = Column(
        Text,
        nullable=True
    )

    createdAt = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updatedAt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    callPrepTopics = Column(ARRAY(String), nullable=True)

    callPrepMaterials = Column(ARRAY(String), nullable=True)

    callPrepSentimentTrend = Column(String, nullable=True)

    callPrepTalkingPoints = Column(ARRAY(String), nullable=True)

    callPrepNextBestAction = Column(Text, nullable=True)
