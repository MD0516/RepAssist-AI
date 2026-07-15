from datetime import datetime

from app.agents.state import AgentState
from app.schemas.interaction import InteractionUpdate, InteractionResponse
from app.services.groqService import llm
from app.services.interactionService import (
    getInteractionById,
    updateInteraction,
)

currentDateTime = datetime.now().isoformat()

structuredLlm = llm.with_structured_output(
    InteractionUpdate
)

SYSTEM_PROMPT = """
You are editing an existing HCP interaction.

You will receive:

1. The current interaction.
2. A user correction or update request.

Rules:

- Update EVERY field explicitly mentioned by the user.
- A single request may contain multiple changes.
- If multiple fields are mentioned, all must be updated.
- Never ignore an explicitly mentioned change.
- Never modify fields the user did not mention.
- Do not infer, assume, or invent values.
- Return only the fields that should change.
- interactionDate must be returned as an ISO-8601 datetime string.
- Use the provided current datetime as the reference point when resolving relative dates.

Date Examples:

If current datetime is:
2026-07-10T15:30:00

Then:
- yesterday -> 2026-07-09T15:30:00
- today -> 2026-07-10T15:30:00
- tomorrow -> 2026-07-11T15:30:00
- last monday -> 2026-07-07T15:30:00
- next friday -> 2026-07-17T15:30:00

Sentiment Rules:

- sentiment must be exactly one of:
    - positive
    - neutral
    - negative

- Always return sentiment values in lowercase.
- Do not return any other sentiment values.

Examples:

User:
"The doctor's name was actually Dr Rajesh Sharma and the sentiment should be positive instead of neutral."

Return:
{
    "hcpName": "Dr Rajesh Sharma",
    "sentiment": "positive"
}

User:
"Change the product to NeuroPlus and mark follow up required."

Return:
{
    "productDiscussed": "NeuroPlus",
    "followUpRequired": true
}

Return only the fields that should be updated.
"""


def editInteraction(
        state: AgentState,
        db,
):
    interaction = getInteractionById(
        db,
        state["interactionId"]
    )

    interactionData = (
        InteractionResponse
        .model_validate(interaction)
        .model_dump()
    )

    response = structuredLlm.invoke(
        f"""
        Current DateTime: 
        {currentDateTime}

        Current Interaction:        
        {interactionData}
        
        User Request:
        
        {state["userMessage"]}
        
        {SYSTEM_PROMPT}
        """
    )

    updates = response.model_dump(
        exclude_unset=True
    )

    updatedInteraction = updateInteraction(
        db=db,
        interaction=interaction,
        updates=updates
    )

    return {
        "interaction": updatedInteraction,
        "metadata": None
    }
