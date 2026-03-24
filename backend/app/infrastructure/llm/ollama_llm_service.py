import json
import re
from typing import Any

import httpx

from app.config import settings
from app.domain.exceptions.extraction_exceptions import LLMUnavailableError
from app.infrastructure.llm.prompts.question_extraction_prompt import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)
from app.interfaces.services.llm_service import ILLMService


class OllamaLLMService(ILLMService):
    """Implementación del servicio LLM usando Ollama (SRP: solo procesa con LLM)."""

    def __init__(self, host: str = None, model: str = None):
        self._host = host or settings.ollama_host
        self._model = model or settings.ollama_model

    async def process(self, text: str) -> dict[str, Any]:
        prompt = USER_PROMPT_TEMPLATE.format(text=text[:8000])  # límite de contexto
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "format": "json",
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self._host}/api/chat",
                    json=payload,
                )
                response.raise_for_status()
        except httpx.ConnectError as exc:
            raise LLMUnavailableError(f"No se pudo conectar a Ollama en {self._host}") from exc
        except httpx.HTTPStatusError as exc:
            raise LLMUnavailableError(f"Ollama respondió con error {exc.response.status_code}") from exc

        raw_content = response.json()["message"]["content"]
        return self._parse_json(raw_content)

    def _parse_json(self, raw: str) -> dict[str, Any]:
        """Extrae JSON de la respuesta del LLM, tolerante a texto extra."""
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not json_match:
            return {"total_preguntas": 0, "preguntas": []}
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            return {"total_preguntas": 0, "preguntas": []}
