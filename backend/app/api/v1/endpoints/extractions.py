from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile

from app.application.dependencies.container import get_extract_use_case, get_result_use_case
from app.application.schemas.document_schema import ProcessingResponse
from app.application.use_cases.extract_questions import ExtractQuestionsUseCase
from app.application.use_cases.get_extraction_result import GetExtractionResultUseCase
from app.domain.value_objects.file_type import FileType

router = APIRouter(prefix="/extractions", tags=["Extractions"])


@router.post("/{document_id}/process", response_model=ProcessingResponse)
async def process_document(
    document_id: UUID,
    file: UploadFile = File(...),
    use_case: ExtractQuestionsUseCase = Depends(get_extract_use_case),
):
    """Procesa un documento ya subido y extrae sus preguntas."""
    file_bytes = await file.read()
    file_type = FileType.from_extension(file.filename).value
    return await use_case.execute(document_id, file_bytes, file_type)


@router.get("/{document_id}", response_model=ProcessingResponse)
async def get_result(
    document_id: UUID,
    use_case: GetExtractionResultUseCase = Depends(get_result_use_case),
):
    """Recupera el resultado de extracción de un documento procesado."""
    return await use_case.execute(document_id)
