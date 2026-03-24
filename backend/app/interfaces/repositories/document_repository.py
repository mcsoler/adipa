from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.application.schemas.document_schema import DocumentResponse


class IDocumentRepository(ABC):
    """Interface del repositorio de documentos (DIP + SRP)."""

    @abstractmethod
    async def save(self, filename: str, file_type: str) -> DocumentResponse:
        ...

    @abstractmethod
    async def find_by_id(self, document_id: UUID) -> Optional[DocumentResponse]:
        ...

    @abstractmethod
    async def update_status(self, document_id: UUID, status: str) -> None:
        ...
