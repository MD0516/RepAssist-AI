from datetime import  datetime

from app.agents.state import AgentState
from app.schemas.interaction import InteractionCreate
from app.services.groqService import llm
from app.services.interactionService import createInteraction

currentDateTime = datetime.now().isoformat()
structuredLlm = llm.with_structured_output(
    InteractionCreate
)


SYSTEM_PROMPT = """
You are an AI CRM assistant for pharmaceutical field representatives.

Extract structured interaction information from the user's message.

Rules:

- Extract only information explicitly mentioned by the user.
- If information is missing, return null or an empty list.
- Do not invent, infer, or assume missing information.
- Materials shared must always be returned as a list of strings.
- followUpRequired should only be true if the user explicitly requests a follow-up action or indicates additional actions are required.
- interactionDate must be returned as an ISO-8601 datetime string.
- Use the provided current datetime as the reference point when resolving relative dates.
- keyDiscussionPoints must be a SINGLE STRING.
- Do NOT return keyDiscussionPoints as an array or list.
- Summarize all discussion points into one text field.
- Multiple discussion points should be combined into one sentence.
- You may use commas to separate multiple points.

Example:

Correct:
"Discussed efficacy data, patient dizziness concerns, and follow-up requirements."

Incorrect:
[
    "efficacy data",
    "patient dizziness concerns",
    "follow-up requirements"
]
    
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
- Positive feedback or interest -> positive
- Neutral discussion -> neutral
- Complaints, adverse events, dissatisfaction, or concerns -> negative

Return only structured interaction data matching the schema.
"""


def logInteraction(
    state: AgentState,
    db,
):
    response = structuredLlm.invoke(
        f"""
        Current DateTime: {currentDateTime}
        {SYSTEM_PROMPT}
        
        User Input:
        {state["userMessage"]}
        """
    )

    interaction = createInteraction(
        db=db,
        interactionData=response.model_dump()
    )

    return interaction