from typing import Optional
from pydantic import BaseModel, Field

from app.domain.value_objects.question_type import QuestionType


class AlternativaSchema(BaseModel):
    letra: str = Field(..., examples=["A"])
    texto: str = Field(..., examples=["Preocupación excesiva difícil de controlar"])


class PreguntaSchema(BaseModel):
    numero: int = Field(..., ge=1)
    enunciado: str = Field(..., min_length=1)
    tipo: QuestionType
    alternativas: list[AlternativaSchema] = Field(default_factory=list)
    respuesta_correcta: Optional[str] = None
