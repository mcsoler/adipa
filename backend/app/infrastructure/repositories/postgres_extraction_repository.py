from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.extraction_model import ExtractionResultModel
from app.interfaces.repositories.extraction_repository import IExtractionRepository


class PostgresExtractionRepository(IExtractionRepository):
    """Implementación concreta del repositorio de resultados de extracción."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, document_id: UUID, result: dict[str, Any]) -> None:
        extraction = ExtractionResultModel(document_id=document_id, result=result)
        self._session.add(extraction)
        await self._session.commit()

    async def find_by_document_id(self, document_id: UUID) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(ExtractionResultModel)
            .where(ExtractionResultModel.document_id == document_id)
            .order_by(ExtractionResultModel.created_at.desc())
        )
        extraction = result.scalar_one_or_none()
        return extraction.result if extraction else None
