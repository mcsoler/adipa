import asyncio
import concurrent.futures

from app.domain.exceptions.extraction_exceptions import LLMUnavailableError
from app.infrastructure.llm.ollama_llm_service import OllamaLLMService
from app.langgraph_workflow.state import WorkflowState


def _run_async(coro):
    """Ejecuta una corutina en un thread separado para evitar conflictos con el event loop de FastAPI."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(asyncio.run, coro)
        return future.result()


def process_with_llm_node(state: WorkflowState) -> WorkflowState:
    """Nodo 2: envía el texto al LLM y obtiene JSON estructurado (SRP)."""
    # Solo omitir si el error viene de un nodo anterior (no de un reintento LLM)
    if state.get("error") and state.get("retry_count", 0) == 0:
        return state

    service = OllamaLLMService()
    try:
        result = _run_async(service.process(state["raw_text"]))
        return {**state, "llm_result": result, "error": None, "retry_count": 0}
    except LLMUnavailableError as exc:
        new_retry = state.get("retry_count", 0) + 1
        return {**state, "retry_count": new_retry, "error": str(exc)}
    except Exception as exc:
        msg = str(exc) or repr(exc)
        return {**state, "llm_result": {}, "error": f"Error en LLM: {msg}", "retry_count": 3}
