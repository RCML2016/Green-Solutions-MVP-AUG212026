"""
Builds and compiles the LangGraph pipeline.

Flow:
  data_normalizer -> diagnostic_reasoner -> [human_review?] -> report_drafter -> END

The routing after diagnostic_reasoner is the "supervisor" behavior:
it reads state["next_step"] (set by the diagnostic node) and decides
whether to detour through human_review or go straight to drafting.
"""

from langgraph.graph import StateGraph, END
from state import PipelineState
from agents import (
    data_normalizer_node,
    diagnostic_reasoner_node,
    report_drafter_node,
    human_review_node,
)


def route_after_diagnosis(state: PipelineState) -> str:
    return "human_review" if state.get("needs_human_review") else "report_drafter"


def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("data_normalizer", data_normalizer_node)
    graph.add_node("diagnostic_reasoner", diagnostic_reasoner_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("report_drafter", report_drafter_node)

    graph.set_entry_point("data_normalizer")
    graph.add_edge("data_normalizer", "diagnostic_reasoner")

    graph.add_conditional_edges(
        "diagnostic_reasoner",
        route_after_diagnosis,
        {
            "human_review": "human_review",
            "report_drafter": "report_drafter",
        },
    )

    graph.add_edge("human_review", "report_drafter")
    graph.add_edge("report_drafter", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    print(app.get_graph().draw_ascii())
