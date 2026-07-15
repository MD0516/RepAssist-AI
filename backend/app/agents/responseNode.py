from app.services.groqService import llm

SYSTEM_PROMPT = """
You are an AI pharmaceutical CRM assistant.

Generate a helpful conversational response based on:

- selected tool
- interaction changes
- metadata
- missing information

Rules:

- Explain what action was performed.
- Mention important extracted information.
- Mention missing information if relevant.
- Be concise and conversational.
- Never return JSON.
- Never mention internal tool names.
"""


def responseNode(state):
    toolResult = state.get("toolResult") or {}

    interaction = (
        toolResult.get("interaction")
        if isinstance(toolResult, dict)
        else None
    )

    metadata = (
        toolResult.get("metadata")
        if isinstance(toolResult, dict)
        else None
    )
    response = llm.invoke(
        f"""
        {SYSTEM_PROMPT}

        User Message:
        {state["userMessage"]}

        Selected Tool:
        {state["selectedTool"]}

        Interaction:
        {interaction}

        Metadata:
        {metadata}
        """
    )

    return {
        "assistantResponse": response.content
    }
