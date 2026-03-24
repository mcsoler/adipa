import asyncio

from app.domain.exceptions.extraction_exceptions import LLMUnavailableError
from app.infrastructure.llm.ollama_llm_service import OllamaLLMService
from app.langgraph_workflow.state import WorkflowState


def process_with_llm_node(state: WorkflowState) -> WorkflowState:
    """Nodo 2: envía el texto al LLM y obtiene JSON estructurado (SRP)."""
    if state.get("error"):
        return state

    service = OllamaLLMService()
    try:
        result = asyncio.get_event_loop().run_until_complete(
            service.process(state["raw_text"])
        )
        return {**state, "llm_result": result, "error": None}
    except LLMUnavailableError as exc:
        retry = state.get("retry_count", 0)
        if retry < 2:
            return {**state, "retry_count": retry + 1, "error": None}
        return {**state, "llm_result": {}, "error": str(exc)}
    except Exception as exc:
        return {**state, "llm_result": {}, "error": f"Error en LLM: {exc}"}
