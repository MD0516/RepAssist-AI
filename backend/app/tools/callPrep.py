from app.schemas.interaction import (
    CallPrepRequest,
    CallPrepSummary,
)

from app.agents.state import AgentState
from app.services.groqService import llm
from app.services.interactionService import getInteractionsByHcp, getInteractionById, updateInteraction

extractLlm = llm.with_structured_output(
    CallPrepRequest
)

summaryLlm = llm.with_structured_output(
    CallPrepSummary
)

EXTRACT_PROMPT = """
You are an AI CRM assistant.

Extract the target HCP name from the user's request.

Examples:

Input:
Prepare me for my next call with Dr Sharma.

Output:
hcpName = Dr Sharma

Input:
What should I discuss with Dr Patel tomorrow?

Output:
hcpName = Dr Patel

Return only:
- hcpName
"""

SUMMARY_PROMPT = """
You are an AI pharmaceutical CRM assistant.

Your task is to prepare a field representative for their next visit.

Analyze the provided historical interactions and generate:

- previousTopics
- materialsAlreadyShared
- sentimentTrend
- talkingPoints
- nextBestAction

Rules:

- Use only information from historical interactions.
- Do not invent interaction history.
- If insufficient history exists, explicitly state that.
- Summarize sentiment trends across interactions.
- Recommended talking points should be practical and relevant.
- Next best action should be concise and actionable.

Return structured output only.
"""


def callPrep(
        state: AgentState,
        db,
):
    if not state["interactionId"]:
        raise Exception(
            "callPrep requires interactionId"
        )

    interaction = getInteractionById(
        db,
        state["interactionId"]
    )

    extractionResult = extractLlm.invoke(
        f"""
        {EXTRACT_PROMPT}

        User Request:

        {state["userMessage"]}
        """
    )

    hcpName = extractionResult.hcpName

    history = getInteractionsByHcp(
        db,
        hcpName,
    )

    historyData = [
        {
            "interactionDate": interaction.interactionDate,
            "interactionType": interaction.interactionType,
            "productDiscussed": interaction.productDiscussed,
            "sentiment": interaction.sentiment,
            "materialsShared": interaction.materialsShared,
            "keyDiscussionPoints": interaction.keyDiscussionPoints,
            "followUpRequired": interaction.followUpRequired,
            "followUpNotes": interaction.followUpNotes,
        }
        for interaction in history
    ]

    prepSummary = summaryLlm.invoke(
        f"""
        {SUMMARY_PROMPT}

        Target HCP:
        {hcpName}

        Historical Interactions:

        {historyData}
        """
    )

    updates = {
        "callPrepTopics": prepSummary.previousTopics,
        "callPrepMaterials": prepSummary.materialsAlreadyShared,
        "callPrepSentimentTrend": prepSummary.sentimentTrend,
        "callPrepTalkingPoints": prepSummary.talkingPoints,
        "callPrepNextBestAction": prepSummary.nextBestAction,
    }
    print(updates)
    updatedInteraction = updateInteraction(
        db,
        interaction,
        updates
    )

    return {
        "interaction": updatedInteraction,

        "metadata": {
            "prepSummary": prepSummary.model_dump(),

            "targetHcp": hcpName,

            "historicalInteractionCount": len(history),
        }
    }
