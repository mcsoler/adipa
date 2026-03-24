from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.document_schema import DocumentResponse
from app.infrastructure.database.models.document_model import DocumentModel
from app.interfaces.repositories.document_repository import IDocumentRepository


class PostgresDocumentRepository(IDocumentRepository):
    """Implementación concreta del repositorio de documentos con PostgreSQL (SRP + DIP)."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, filename: str, file_type: str) -> DocumentResponse:
        document = DocumentModel(filename=filename, file_type=file_type, status="pending")
        self._session.add(document)
        await self._session.commit()
        await self._session.refresh(document)
        return DocumentResponse.model_validate(document)

    async def find_by_id(self, document_id: UUID) -> DocumentResponse | None:
        result = await self._session.execute(
            select(DocumentModel).where(DocumentModel.id == document_id)
        )
        document = result.scalar_one_or_none()
        return DocumentResponse.model_validate(document) if document else None

    async def update_status(self, document_id: UUID, status: str) -> None:
        await self._session.execute(
            update(DocumentModel)
            .where(DocumentModel.id == document_id)
            .values(status=status)
        )
        await self._session.commit()
