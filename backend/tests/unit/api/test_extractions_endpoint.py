"""
TDD - RED PHASE
Tests de los endpoints de extracción.
"""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.application.schemas.document_schema import ProcessingResponse


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


_SAMPLE_RESULT = {
    "total_preguntas": 1,
    "preguntas": [{
        "numero": 1,
        "enunciado": "¿Qué es el TAG?",
        "tipo": "seleccion_multiple",
        "alternativas": [{"letra": "A", "texto": "Trastorno de ansiedad"}],
        "respuesta_correcta": "A",
    }]
}


# ── RED 1: procesar documento existente retorna 200 con resultado ─────────
@pytest.mark.asyncio
async def test_process_document_returns_200_with_result(client):
    doc_id = uuid4()
    mock_result = ProcessingResponse(
        document_id=doc_id,
        status="completed",
        result=_SAMPLE_RESULT,
    )

    with patch(
        "app.application.use_cases.extract_questions.ExtractQuestionsUseCase.execute",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await client.post(
            f"/api/v1/extractions/{doc_id}/process",
            files={"file": ("examen.pdf", b"%PDF contenido", "application/pdf")},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["result"]["total_preguntas"] == 1


# ── RED 2: obtener resultado existente retorna datos correctos ─────────────
@pytest.mark.asyncio
async def test_get_extraction_result_returns_stored_data(client):
    doc_id = uuid4()
    mock_result = ProcessingResponse(
        document_id=doc_id,
        status="completed",
        result=_SAMPLE_RESULT,
    )

    with patch(
        "app.application.use_cases.get_extraction_result.GetExtractionResultUseCase.execute",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await client.get(f"/api/v1/extractions/{doc_id}")

    assert response.status_code == 200
    assert response.json()["result"]["total_preguntas"] == 1


# ── RED 3: documento no encontrado retorna status not_found ───────────────
@pytest.mark.asyncio
async def test_get_nonexistent_document_returns_not_found(client):
    doc_id = uuid4()
    mock_result = ProcessingResponse(
        document_id=doc_id,
        status="not_found",
        error="Documento no encontrado.",
    )

    with patch(
        "app.application.use_cases.get_extraction_result.GetExtractionResultUseCase.execute",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await client.get(f"/api/v1/extractions/{doc_id}")

    assert response.status_code == 200
    assert response.json()["status"] == "not_found"


# ── RED 4: health check retorna 200 ──────────────────────────────────────
@pytest.mark.asyncio
async def test_health_check_returns_ok(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
