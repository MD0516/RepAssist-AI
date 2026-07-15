from typing import TypedDict, Optional, Any


class AgentState(TypedDict):
    userMessage: str

    interactionId: Optional[str]

    currentInteraction: Optional[dict]

    selectedTool: Optional[str]

    toolResult: Optional[Any]

    assistantResponse: Optional[str]

    db: Any