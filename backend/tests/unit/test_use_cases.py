import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.application.schemas.document_schema import DocumentResponse
from app.application.use_cases.upload_document import UploadDocumentUseCase
from app.domain.exceptions.document_exceptions import FileTooLargeError, UnsupportedFileTypeError


@pytest.fixture
def mock_doc_repo():
    repo = AsyncMock()
    repo.save.return_value = DocumentResponse(
        id=uuid4(),
        filename="test.pdf",
        file_type="pdf",
        status="pending",
        uploaded_at=__import__("datetime").datetime.now(),
    )
    return repo


@pytest.mark.asyncio
async def test_upload_valid_pdf(mock_doc_repo):
    use_case = UploadDocumentUseCase(mock_doc_repo)
    result = await use_case.execute("examen.pdf", b"fake_pdf_content")

    assert result.filename == "test.pdf"
    assert result.status == "pending"
    mock_doc_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_upload_unsupported_format_raises(mock_doc_repo):
    use_case = UploadDocumentUseCase(mock_doc_repo)
    with pytest.raises(UnsupportedFileTypeError):
        await use_case.execute("examen.pptx", b"content")


@pytest.mark.asyncio
async def test_upload_file_too_large_raises(mock_doc_repo):
    use_case = UploadDocumentUseCase(mock_doc_repo)
    big_file = b"x" * (60 * 1024 * 1024)  # 60MB
    with pytest.raises(FileTooLargeError):
        await use_case.execute("examen.pdf", big_file)
