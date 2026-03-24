"""
TDD - RED PHASE
Tests del nodo validate_output_node.
"""
from app.langgraph_workflow.nodes.validate_output_node import validate_output_node
from app.langgraph_workflow.state import WorkflowState


def _base_state(**kwargs) -> WorkflowState:
    return WorkflowState(
        file_bytes=b"",
        file_type="pdf",
        raw_text="texto",
        llm_result={},
        validated_result={},
        error=None,
        retry_count=0,
        **kwargs,
    )


_VALID_RESULT = {
    "total_preguntas": 1,
    "preguntas": [{
        "numero": 1,
        "enunciado": "¿Qué es el TAG?",
        "tipo": "seleccion_multiple",
        "alternativas": [{"letra": "A", "texto": "Trastorno de ansiedad"}],
        "respuesta_correcta": "A",
    }]
}


# ── RED 1: JSON válido pasa validación sin cambios ────────────────────────
def test_validate_node_passes_valid_result():
    state = _base_state(llm_result=_VALID_RESULT)
    result = validate_output_node(state)

    assert result["validated_result"]["total_preguntas"] == 1
    assert len(result["validated_result"]["preguntas"]) == 1
    assert result["error"] is None


# ── RED 2: si el estado tiene error previo, retorna vacío sin crash ───────
def test_validate_node_returns_empty_on_prior_error():
    state = _base_state(error="error previo", llm_result={})
    result = validate_output_node(state)

    assert result["validated_result"] == {"total_preguntas": 0, "preguntas": []}


# ── RED 3: preguntas con campo inválido son filtradas (rescate parcial) ───
def test_validate_node_filters_invalid_questions():
    llm_result = {
        "total_preguntas": 2,
        "preguntas": [
            {   # válida
                "numero": 1,
                "enunciado": "¿Pregunta válida?",
                "tipo": "verdadero_falso",
                "alternativas": [],
                "respuesta_correcta": "Verdadero",
            },
            {   # inválida: falta "enunciado"
                "numero": 2,
                "tipo": "desarrollo",
            },
        ]
    }
    state = _base_state(llm_result=llm_result)
    result = validate_output_node(state)

    # solo la pregunta válida debe quedar
    assert result["validated_result"]["total_preguntas"] == 1
    assert result["validated_result"]["preguntas"][0]["numero"] == 1


# ── RED 4: JSON completamente inválido retorna 0 preguntas sin crash ──────
def test_validate_node_handles_completely_invalid_json():
    state = _base_state(llm_result={"garbage": "data", "no_schema": True})
    result = validate_output_node(state)

    assert result["validated_result"]["total_preguntas"] == 0
    assert result["validated_result"]["preguntas"] == []
    assert result["error"] is None
