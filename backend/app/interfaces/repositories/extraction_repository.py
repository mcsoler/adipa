from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import UUID


class IExtractionRepository(ABC):
    """Interface del repositorio de resultados de extracción."""

    @abstractmethod
    async def save(self, document_id: UUID, result: dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def find_by_document_id(self, document_id: UUID) -> Optional[dict[str, Any]]:
        ...
