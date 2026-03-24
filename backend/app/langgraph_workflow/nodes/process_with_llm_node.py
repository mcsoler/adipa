import asyncio

from app.domain.exceptions.extraction_exceptions import LLMUnavailableError
from app.infrastructure.llm.ollama_llm_service import OllamaLLMService
from app.langgraph_workflow.state import WorkflowState


def process_with_llm_node(state: WorkflowState) -> WorkflowState:
    """Nodo 2: envía el texto al LLM y obtiene JSON estructurado (SRP)."""
    # Solo omitir si el error viene de un nodo anterior (no de un reintento LLM)
    if state.get("error") and state.get("retry_count", 0) == 0:
        return state

    service = OllamaLLMService()
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(service.process(state["raw_text"]))
        loop.close()
        return {**state, "llm_result": result, "error": None, "retry_count": 0}
    except LLMUnavailableError as exc:
        new_retry = state.get("retry_count", 0) + 1
        return {**state, "retry_count": new_retry, "error": str(exc)}
    except Exception as exc:
        return {**state, "llm_result": {}, "error": f"Error en LLM: {exc}", "retry_count": 3}
