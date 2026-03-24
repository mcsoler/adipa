"""
TDD - RED PHASE
Tests de los endpoints HTTP escritos antes de verificar integración completa.
Usan mocks para aislar la capa HTTP del dominio.
"""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.application.schemas.document_schema import DocumentUploadResponse
from app.domain.exceptions.document_exceptions import UnsupportedFileTypeError, FileTooLargeError


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


# ── RED 1: subir PDF válido retorna 201 con document_id ───────────────────
@pytest.mark.asyncio
async def test_upload_valid_pdf_returns_201(client):
    mock_result = DocumentUploadResponse(
        document_id=uuid4(),
        filename="examen.pdf",
        status="pending",
        message="Documento recibido.",
    )

    with patch(
        "app.application.use_cases.upload_document.UploadDocumentUseCase.execute",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await client.post(
            "/api/v1/documents/upload",
            files={"file": ("examen.pdf", b"%PDF-1.4 contenido", "application/pdf")},
        )

    assert response.status_code == 201
    body = response.json()
    assert "document_id" in body
    assert body["status"] == "pending"


# ── RED 2: subir formato no soportado retorna 415 ─────────────────────────
@pytest.mark.asyncio
async def test_upload_unsupported_format_returns_415(client):
    with patch(
        "app.application.use_cases.upload_document.UploadDocumentUseCase.execute",
        new_callable=AsyncMock,
        side_effect=UnsupportedFileTypeError("pptx"),
    ):
        response = await client.post(
            "/api/v1/documents/upload",
            files={"file": ("slides.pptx", b"contenido", "application/vnd.ms-powerpoint")},
        )

    assert response.status_code == 415
    assert "pptx" in response.json()["detail"].lower() or "soportado" in response.json()["detail"].lower()


# ── RED 3: archivo demasiado grande retorna 413 ───────────────────────────
@pytest.mark.asyncio
async def test_upload_too_large_returns_413(client):
    with patch(
        "app.application.use_cases.upload_document.UploadDocumentUseCase.execute",
        new_callable=AsyncMock,
        side_effect=FileTooLargeError(60.0, 50),
    ):
        response = await client.post(
            "/api/v1/documents/upload",
            files={"file": ("big.pdf", b"x" * 10, "application/pdf")},
        )

    assert response.status_code == 413


# ── RED 4: petición sin archivo retorna 422 de FastAPI ────────────────────
@pytest.mark.asyncio
async def test_upload_without_file_returns_422(client):
    response = await client.post("/api/v1/documents/upload")
    assert response.status_code == 422
