from pydantic import BaseModel, Field
from app.application.schemas.question_schema import PreguntaSchema


class ExtractionResultSchema(BaseModel):
    total_preguntas: int = Field(..., ge=0)
    preguntas: list[PreguntaSchema] = Field(default_factory=list)

    model_config = {"json_schema_extra": {
        "example": {
            "total_preguntas": 1,
            "preguntas": [{
                "numero": 1,
                "enunciado": "¿Cuál es el principal criterio diagnóstico del TAG?",
                "tipo": "seleccion_multiple",
                "alternativas": [
                    {"letra": "A", "texto": "Alucinaciones visuales recurrentes"},
                    {"letra": "B", "texto": "Preocupación excesiva difícil de controlar"},
                ],
                "respuesta_correcta": "B"
            }]
        }
    }}
