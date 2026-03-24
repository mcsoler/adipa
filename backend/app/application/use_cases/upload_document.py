from app.application.schemas.document_schema import DocumentUploadResponse
from app.config import settings
from app.domain.exceptions.document_exceptions import FileTooLargeError, UnsupportedFileTypeError
from app.domain.value_objects.file_type import FileType
from app.interfaces.repositories.document_repository import IDocumentRepository


class UploadDocumentUseCase:
    """Caso de uso: validar y persistir un documento subido (SRP)."""

    def __init__(self, document_repo: IDocumentRepository):
        self._repo = document_repo

    async def execute(self, filename: str, file_bytes: bytes) -> DocumentUploadResponse:
        size_mb = len(file_bytes) / (1024 * 1024)
        if size_mb > settings.max_file_size_mb:
            raise FileTooLargeError(size_mb, settings.max_file_size_mb)

        try:
            file_type = FileType.from_extension(filename)
        except ValueError as exc:
            raise UnsupportedFileTypeError(filename.rsplit(".", 1)[-1]) from exc

        document = await self._repo.save(filename, file_type.value)

        return DocumentUploadResponse(
            document_id=document.id,
            filename=document.filename,
            status=document.status,
            message="Documento recibido. Llama a /process para extraer preguntas.",
        )
