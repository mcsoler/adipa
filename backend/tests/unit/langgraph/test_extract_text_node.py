"""
TDD - RED PHASE
Tests escritos ANTES de verificar la implementación.
Definen el contrato esperado del nodo extract_text_node.
"""
import io
import pytest
from unittest.mock import patch, MagicMock

from app.langgraph_workflow.nodes.extract_text_node import extract_text_node
from app.langgraph_workflow.state import WorkflowState


def _base_state(**kwargs) -> WorkflowState:
    return WorkflowState(
        file_bytes=b"",
        file_type="pdf",
        raw_text="",
        llm_result={},
        validated_result={},
        error=None,
        retry_count=0,
        **kwargs,
    )


# ── RED 1: tipo de archivo soportado extrae texto ──────────────────────────
def test_extract_text_node_returns_raw_text_for_supported_type():
    mock_extractor = MagicMock()
    mock_extractor.extract.return_value = "¿Cuál es el TAG? A) Ansiedad B) Depresión"

    with patch(
        "app.langgraph_workflow.nodes.extract_text_node.ExtractorFactory.get",
        return_value=mock_extractor,
    ):
        state = _base_state(file_bytes=b"fake_pdf", file_type="pdf")
        result = extract_text_node(state)

    assert result["raw_text"] == "¿Cuál es el TAG? A) Ansiedad B) Depresión"
    assert result["error"] is None


# ── RED 2: tipo no soportado pone error en estado ─────────────────────────
def test_extract_text_node_sets_error_for_unsupported_type():
    state = _base_state(file_bytes=b"fake", file_type="pptx")
    result = extract_text_node(state)

    assert result["raw_text"] == ""
    assert result["error"] is not None
    assert "pptx" in result["error"].lower() or "soportado" in result["error"].lower()


# ── RED 3: documento vacío pone error ─────────────────────────────────────
def test_extract_text_node_sets_error_for_empty_document():
    mock_extractor = MagicMock()
    mock_extractor.extract.return_value = "   "  # solo espacios

    with patch(
        "app.langgraph_workflow.nodes.extract_text_node.ExtractorFactory.get",
        return_value=mock_extractor,
    ):
        state = _base_state(file_bytes=b"empty_pdf", file_type="pdf")
        result = extract_text_node(state)

    assert result["raw_text"] == ""
    assert result["error"] is not None


# ── RED 4: excepción inesperada no propaga, se captura en error ───────────
def test_extract_text_node_catches_unexpected_exceptions():
    mock_extractor = MagicMock()
    mock_extractor.extract.side_effect = RuntimeError("fallo inesperado")

    with patch(
        "app.langgraph_workflow.nodes.extract_text_node.ExtractorFactory.get",
        return_value=mock_extractor,
    ):
        state = _base_state(file_bytes=b"bad_pdf", file_type="pdf")
        result = extract_text_node(state)

    assert result["error"] is not None
    assert "error" in result["error"].lower() or "fallo" in result["error"].lower()
