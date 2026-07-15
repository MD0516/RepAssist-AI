from app.agents.state import AgentState
from app.schemas.interaction import (
    InteractionFilters,
    InteractionResponse,
)
from app.services.groqService import llm
from app.services.interactionService import (
    filterInteractions,
)

structedLlm = llm.with_structured_output(
    InteractionFilters
)

SYSTEM_PROMPT = """
You are an AI CRM search assistant.

Extract interaction search filters from the user's request.

Possible filters:

- hcpName
- productDiscussed
- interactionType
- sentiment
- materialsShared
- startDate
- endDate

Rules:

- Extract only explicitly requested filters.
- Leave missing fields as null.
- Convert relative dates into actual datetime values.
- Return output matching the provided schema exactly.
"""

def listInteractions(
        state: AgentState,
        db
):
    filters = structedLlm.invoke(
        f"""
        {SYSTEM_PROMPT}
        
        User Request:
        {state["userMessage"]}
        """
    )

    results = filterInteractions(
        db,
        filters
    )

    interactionList = [
        InteractionResponse
        .model_validate(
            interaction
        )
        .model_dump()

        for interaction in results
    ]

    return {
        "interaction": None,

        "metadata": {
            "interactionList": interactionList,
            "count": len(interactionList),
        }
    }