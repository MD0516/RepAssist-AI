from app.agents.router import routeTool
from app.agents.state import AgentState
from app.tools.logInteraction import logInteraction
from app.tools.editInteraction import editInteraction
from app.tools.suggestFollowUp import suggestFollowUp
from app.tools.callPrep import callPrep
from app.tools.listInteractions import listInteractions


def routerNode(state: AgentState):
    selectedTool = routeTool(
        state["userMessage"],
        state["interactionId"],
    )

    return {
        "selectedTool": selectedTool
    }


def toolNode(state: AgentState):
    selectedTool = state["selectedTool"]

    toolMap = {
        "logInteraction": logInteraction,
        "editInteraction": editInteraction,
        "suggestFollowUp": suggestFollowUp,
        "callPrep": callPrep,
        "listInteractions": listInteractions,
    }

    toolFunction = toolMap.get(selectedTool)

    if not toolFunction:
        return {
            "assistantResponse": "Unable to determine the correct tool"
        }

    result = toolFunction(
        state,
        state["db"]
    )

    return {
        "toolResult": result
    }