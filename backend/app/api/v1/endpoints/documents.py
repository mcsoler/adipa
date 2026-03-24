from fastapi import APIRouter, Depends, File, UploadFile

from app.application.dependencies.container import get_upload_use_case
from app.application.schemas.document_schema import DocumentUploadResponse
from app.application.use_cases.upload_document import UploadDocumentUseCase

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    use_case: UploadDocumentUseCase = Depends(get_upload_use_case),
):
    """Sube un documento PDF, DOCX o XLSX para procesamiento."""
    file_bytes = await file.read()
    return await use_case.execute(file.filename, file_bytes)
