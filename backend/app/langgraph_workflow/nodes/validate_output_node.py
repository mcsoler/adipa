from app.application.schemas.extraction_schema import ExtractionResultSchema
from app.langgraph_workflow.state import WorkflowState


def validate_output_node(state: WorkflowState) -> WorkflowState:
    """Nodo 3: valida el JSON del LLM contra el schema Pydantic (SRP)."""
    if state.get("error"):
        return {**state, "validated_result": {"total_preguntas": 0, "preguntas": []}}

    try:
        validated = ExtractionResultSchema.model_validate(state.get("llm_result", {}))
        return {**state, "validated_result": validated.model_dump(), "error": None}
    except Exception:
        # Intento de rescate: usar solo preguntas válidas
        raw = state.get("llm_result", {})
        preguntas_raw = raw.get("preguntas", [])
        valid_preguntas = []

        for p in preguntas_raw:
            try:
                from app.application.schemas.question_schema import PreguntaSchema
                PreguntaSchema.model_validate(p)
                valid_preguntas.append(p)
            except Exception:
                continue

        result = {"total_preguntas": len(valid_preguntas), "preguntas": valid_preguntas}
        return {**state, "validated_result": result, "error": None}
