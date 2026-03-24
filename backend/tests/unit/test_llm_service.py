import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.infrastructure.llm.ollama_llm_service import OllamaLLMService
from app.domain.exceptions.extraction_exceptions import LLMUnavailableError


@pytest.mark.asyncio
async def test_process_returns_valid_json():
    service = OllamaLLMService(host="http://localhost:11434", model="llama3")
    expected = {
        "total_preguntas": 1,
        "preguntas": [{
            "numero": 1,
            "enunciado": "¿Qué es el TAG?",
            "tipo": "seleccion_multiple",
            "alternativas": [{"letra": "A", "texto": "Trastorno de ansiedad generalizada"}],
            "respuesta_correcta": "A",
        }]
    }

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "message": {"content": json.dumps(expected)}
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response):
        result = await service.process("¿Qué es el TAG?\nA) Trastorno de ansiedad generalizada")

    assert result["total_preguntas"] == 1
    assert len(result["preguntas"]) == 1


@pytest.mark.asyncio
async def test_process_raises_on_connection_error():
    import httpx
    service = OllamaLLMService(host="http://invalid-host:11434", model="llama3")

    with patch("httpx.AsyncClient.post", side_effect=httpx.ConnectError("connection refused")):
        with pytest.raises(LLMUnavailableError):
            await service.process("texto")


def test_parse_json_tolerates_extra_text():
    service = OllamaLLMService()
    raw = 'Aquí está el resultado:\n{"total_preguntas": 0, "preguntas": []}\nEspero que ayude.'
    result = service._parse_json(raw)
    assert result["total_preguntas"] == 0
