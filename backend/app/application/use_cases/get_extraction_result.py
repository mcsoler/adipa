from uuid import UUID

from app.application.schemas.document_schema import ProcessingResponse
from app.interfaces.repositories.document_repository import IDocumentRepository
from app.interfaces.repositories.extraction_repository import IExtractionRepository


class GetExtractionResultUseCase:
    """Caso de uso: recuperar el resultado de extracción almacenado (SRP)."""

    def __init__(
        self,
        document_repo: IDocumentRepository,
        extraction_repo: IExtractionRepository,
    ):
        self._doc_repo = document_repo
        self._ext_repo = extraction_repo

    async def execute(self, document_id: UUID) -> ProcessingResponse:
        document = await self._doc_repo.find_by_id(document_id)
        if not document:
            return ProcessingResponse(
                document_id=document_id,
                status="not_found",
                error="Documento no encontrado.",
            )

        result = await self._ext_repo.find_by_document_id(document_id)
        return ProcessingResponse(
            document_id=document_id,
            status=document.status,
            result=result,
        )
