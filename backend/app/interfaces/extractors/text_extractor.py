from abc import ABC, abstractmethod


class ITextExtractor(ABC):
    """Interface de extracción de texto (ISP: una sola responsabilidad).
    Cualquier nuevo formato debe implementar solo este método."""

    @abstractmethod
    def extract(self, file_bytes: bytes) -> str:
        """Extrae el texto plano de los bytes del archivo."""
        ...
