from langgraph.graph import StateGraph, END

from app.langgraph_workflow.state import WorkflowState
from app.langgraph_workflow.nodes.extract_text_node import extract_text_node
from app.langgraph_workflow.nodes.process_with_llm_node import process_with_llm_node
from app.langgraph_workflow.nodes.validate_output_node import validate_output_node


def should_retry(state: WorkflowState) -> str:
    """Enrutador condicional: si hay error por LLM y quedan reintentos, vuelve a intentar."""
    if state.get("error") and state.get("retry_count", 0) < 2:
        return "process_with_llm"
    return "validate_output"


def build_extraction_graph() -> StateGraph:
    graph = StateGraph(WorkflowState)

    graph.add_node("extract_text", extract_text_node)
    graph.add_node("process_with_llm", process_with_llm_node)
    graph.add_node("validate_output", validate_output_node)

    graph.set_entry_point("extract_text")
    graph.add_edge("extract_text", "process_with_llm")
    graph.add_conditional_edges(
        "process_with_llm",
        should_retry,
        {
            "process_with_llm": "process_with_llm",
            "validate_output": "validate_output",
        },
    )
    graph.add_edge("validate_output", END)

    return graph.compile()


extraction_graph = build_extraction_graph()
