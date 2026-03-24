import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock

from app.main import app
from app.application.dependencies.container import (
    get_upload_use_case,
    get_extract_use_case,
    get_result_use_case,
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_upload_use_case():
    return AsyncMock()


@pytest.fixture
def mock_extract_use_case():
    return AsyncMock()


@pytest.fixture
def mock_result_use_case():
    return AsyncMock()


@pytest.fixture
def sample_pdf_bytes() -> bytes:
    """Bytes mínimos de PDF válido para tests."""
    return (
        b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
        b"xref\n0 4\n0000000000 65535 f\n"
        b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n0\n%%EOF"
    )


@pytest.fixture
def sample_extraction_result() -> dict:
    return {
        "total_preguntas": 1,
        "preguntas": [{
            "numero": 1,
            "enunciado": "¿Cuál es el principal criterio diagnóstico del TAG?",
            "tipo": "seleccion_multiple",
            "alternativas": [
                {"letra": "A", "texto": "Alucinaciones visuales recurrentes"},
                {"letra": "B", "texto": "Preocupación excesiva difícil de controlar"},
            ],
            "respuesta_correcta": "B",
        }]
    }
