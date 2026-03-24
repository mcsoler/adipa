from app.domain.exceptions.document_exceptions import UnsupportedFileTypeError
from app.domain.value_objects.file_type import FileType
from app.infrastructure.extractors.docx_extractor import DocxExtractor
from app.infrastructure.extractors.pdf_extractor import PdfExtractor
from app.infrastructure.extractors.xlsx_extractor import XlsxExtractor
from app.interfaces.extractors.text_extractor import ITextExtractor


class ExtractorFactory:
    """Factory que retorna el extractor correcto por tipo de archivo.
    OCP: para agregar un nuevo formato solo se registra aquí sin modificar otros extractores."""

    _registry: dict[FileType, type[ITextExtractor]] = {
        FileType.PDF: PdfExtractor,
        FileType.DOCX: DocxExtractor,
        FileType.XLSX: XlsxExtractor,
    }

    @classmethod
    def get(cls, file_type: FileType) -> ITextExtractor:
        extractor_class = cls._registry.get(file_type)
        if not extractor_class:
            raise UnsupportedFileTypeError(file_type.value)
        return extractor_class()
