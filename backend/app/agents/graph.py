from langgraph.graph import StateGraph, END

from app.agents.nodes import routerNode, toolNode
from app.agents.responseNode import responseNode
from app.agents.state import AgentState

workflow = StateGraph(AgentState)

workflow.add_node(
    "router",
    routerNode
)
workflow.add_node(
    "toolExecutor",
    toolNode
)
workflow.add_node(
    'responseGenerator',
    responseNode
)

workflow.set_entry_point(
    "router",
)

workflow.add_edge(
    "router",
    "toolExecutor",
)

workflow.add_edge(
    "toolExecutor",
    "responseGenerator"
)

workflow.add_edge(
    "responseGenerator",
    END
)

graph = workflow.compile()
