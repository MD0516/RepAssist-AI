from app.schemas.interaction import FollowUpSuggestion
from app.services.groqService import llm
from app.services.interactionService import getInteractionById, updateInteraction

structuredLlm = llm.with_structured_output(
    FollowUpSuggestion
)

SYSTEM_PROMPT = """
You are an AI pharmaceutical CRM assistant.

Analyze the interaction and suggest the most appropriate follow-up action.

Consider:
- HCP sentiment
- product interest level
- discussion points
- followUpRequired
- materials shared

Rules:
- Base recommendations strictly on the interaction data.
- If followUpRequired is false and the HCP did not request additional information, avoid suggesting mandatory follow-up meetings.
- If the HCP showed strong interest or requested additional information, suggest appropriate next actions.
- If the interaction was neutral and complete, a recommendation of "No immediate follow-up required" is acceptable.
- Do not invent requests or concerns that are not present in the interaction.

Return:
- suggestedAction
- reasoning
"""

def suggestFollowUp(
    state,
    db,
):
    interaction = getInteractionById(
        db,
        state["interactionId"]
    )

    response = structuredLlm.invoke(
        f"""
        Interaction:
        
        {interaction.__dict__}
        
        {SYSTEM_PROMPT}
        """
    )

    updates = {
        "followUpRequired": True,
        "followUpNotes": response.suggestedAction,
    }

    updatedInteraction = updateInteraction(
        db=db,
        interaction=interaction,
        updates=updates,
    )

    return {
        "interaction": updatedInteraction,
        "metadata": response.model_dump()
    }