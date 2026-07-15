from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from uuid import UUID


class InteractionBase(BaseModel):
    hcpName: Optional[str] = None
    interactionDate: Optional[datetime] = None
    interactionType: Optional[str] = None
    productDiscussed: Optional[str] = None
    sentiment: Optional[str] = None
    materialsShared: List[str] = []
    keyDiscussionPoints: Optional[str] = None
    followUpRequired: bool = False
    followUpNotes: Optional[str] = None
    callPrepTopics: list[str] | None = None
    callPrepMaterials: list[str] | None = None
    callPrepSentimentTrend: str | None = None
    callPrepTalkingPoints: list[str] | None = None
    callPrepNextBestAction: str | None = None


class InteractionCreate(InteractionBase):
    pass


class InteractionResponse(
    InteractionBase
):
    id: UUID
    createdAt: datetime
    updatedAt: datetime

    model_config = {
        "from_attributes": True
    }


class InteractionUpdate(BaseModel):
    hcpName: str | None = None
    interactionDate: datetime | None = None
    interactionType: str | None = None
    productDiscussed: str | None = None
    sentiment: str | None = None
    materialsShared: list[str] | None = None
    keyDiscussionPoints: str | None = None
    followUpRequired: bool | None = None
    followUpNotes: str | None = None
    callPrepTopics: list[str] | None = None
    callPrepMaterials: list[str] | None = None
    callPrepSentimentTrend: str | None = None
    callPrepTalkingPoints: list[str] | None = None
    callPrepNextBestAction: str | None = None


class FollowUpSuggestion(BaseModel):
    suggestedAction: str
    reasoning: str


class CallPrepRequest(BaseModel):
    hcpName: str


class CallPrepSummary(BaseModel):
    previousTopics: list[str]

    materialsAlreadyShared: list[str]

    sentimentTrend: str

    talkingPoints: list[str]

    nextBestAction: str


class InteractionFilters(BaseModel):
    hcpName: Optional[str] = None
    productDiscussed: Optional[str] = None
    sentiment: Optional[str] = None
    interactionType: Optional[str] = None
    lookbackDays: Optional[int] = Field(
        None,
        description="Number of days to look back from today, e.g. 14 for 'last two weeks', 7 for 'this week', 1 for 'today'. Null if no time range mentioned."
    )
