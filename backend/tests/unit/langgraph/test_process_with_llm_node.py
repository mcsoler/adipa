"""
TDD - RED PHASE
Tests del nodo process_with_llm_node.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.langgraph_workflow.nodes.process_with_llm_node import process_with_llm_node
from app.langgraph_workflow.state import WorkflowState


def _base_state(**kwargs) -> WorkflowState:
    return WorkflowState(
        file_bytes=b"",
        file_type="pdf",
        raw_text="¿Cuál es el TAG? A) Ansiedad B) Depresión",
        llm_result={},
        validated_result={},
        error=None,
        retry_count=0,
        **kwargs,
    )


_VALID_LLM_RESULT = {
    "total_preguntas": 1,
    "preguntas": [{
        "numero": 1,
        "enunciado": "¿Cuál es el TAG?",
        "tipo": "seleccion_multiple",
        "alternativas": [{"letra": "A", "texto": "Ansiedad"}],
        "respuesta_correcta": "A",
    }]
}


# ── RED 1: cuando no hay error previo, llama al LLM y guarda resultado ────
def test_process_node_calls_llm_and_stores_result():
    mock_service = MagicMock()
    mock_service.process = AsyncMock(return_value=_VALID_LLM_RESULT)

    with patch(
        "app.langgraph_workflow.nodes.process_with_llm_node.OllamaLLMService",
        return_value=mock_service,
    ):
        result = process_with_llm_node(_base_state())

    assert result["llm_result"] == _VALID_LLM_RESULT
    assert result["error"] is None


# ── RED 2: si el estado ya tiene error, no llama al LLM (cortocircuito) ──
def test_process_node_skips_llm_when_error_exists():
    mock_service = MagicMock()
    mock_service.process = AsyncMock(return_value=_VALID_LLM_RESULT)

    with patch(
        "app.langgraph_workflow.nodes.process_with_llm_node.OllamaLLMService",
        return_value=mock_service,
    ):
        state = _base_state(error="error previo del extractor")
        result = process_with_llm_node(state)

    mock_service.process.assert_not_called()
    assert result["error"] == "error previo del extractor"


# ── RED 3: LLM no disponible incrementa retry_count (hasta 2 veces) ──────
def test_process_node_increments_retry_on_llm_unavailable():
    from app.domain.exceptions.extraction_exceptions import LLMUnavailableError

    mock_service = MagicMock()
    mock_service.process = AsyncMock(side_effect=LLMUnavailableError("Ollama caído"))

    with patch(
        "app.langgraph_workflow.nodes.process_with_llm_node.OllamaLLMService",
        return_value=mock_service,
    ):
        state = _base_state(retry_count=0)
        result = process_with_llm_node(state)

    assert result["retry_count"] == 1
    assert result["error"] is None  # no error aún, puede reintentar


# ── RED 4: después de 2 reintentos, propaga el error ─────────────────────
def test_process_node_sets_error_after_max_retries():
    from app.domain.exceptions.extraction_exceptions import LLMUnavailableError

    mock_service = MagicMock()
    mock_service.process = AsyncMock(side_effect=LLMUnavailableError("Ollama caído"))

    with patch(
        "app.langgraph_workflow.nodes.process_with_llm_node.OllamaLLMService",
        return_value=mock_service,
    ):
        state = _base_state(retry_count=2)
        result = process_with_llm_node(state)

    assert result["error"] is not None
    assert "ollama" in result["error"].lower() or "llm" in result["error"].lower()
