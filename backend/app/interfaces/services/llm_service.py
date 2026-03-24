from abc import ABC, abstractmethod
from typing import Any


class ILLMService(ABC):
    """Interface del servicio LLM (DIP: depender de abstracción, no implementación)."""

    @abstractmethod
    async def process(self, text: str) -> dict[str, Any]:
        """Procesa texto crudo y retorna JSON estructurado con preguntas detectadas."""
        ...
