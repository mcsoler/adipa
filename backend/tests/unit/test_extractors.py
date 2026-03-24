import io
import pytest

from app.domain.exceptions.document_exceptions import UnsupportedFileTypeError
from app.domain.value_objects.file_type import FileType
from app.infrastructure.extractors.extractor_factory import ExtractorFactory
from app.infrastructure.extractors.xlsx_extractor import XlsxExtractor


def test_factory_returns_pdf_extractor():
    extractor = ExtractorFactory.get(FileType.PDF)
    from app.infrastructure.extractors.pdf_extractor import PdfExtractor
    assert isinstance(extractor, PdfExtractor)


def test_factory_returns_docx_extractor():
    extractor = ExtractorFactory.get(FileType.DOCX)
    from app.infrastructure.extractors.docx_extractor import DocxExtractor
    assert isinstance(extractor, DocxExtractor)


def test_factory_returns_xlsx_extractor():
    extractor = ExtractorFactory.get(FileType.XLSX)
    assert isinstance(extractor, XlsxExtractor)


def test_file_type_from_extension_pdf():
    assert FileType.from_extension("examen.pdf") == FileType.PDF


def test_file_type_from_extension_docx():
    assert FileType.from_extension("examen.docx") == FileType.DOCX


def test_file_type_from_extension_xlsx():
    assert FileType.from_extension("examen.xlsx") == FileType.XLSX


def test_file_type_unsupported_raises():
    with pytest.raises(ValueError):
        FileType.from_extension("examen.pptx")


def test_xlsx_extractor_extracts_text():
    """Test con un XLSX generado en memoria."""
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.append(["Pregunta", "Alternativa A", "Alternativa B"])
    ws.append(["¿Qué es el TAG?", "Trastorno de ansiedad", "Trastorno del ánimo"])
    buffer = io.BytesIO()
    wb.save(buffer)

    extractor = XlsxExtractor()
    result = extractor.extract(buffer.getvalue())

    assert "Pregunta" in result
    assert "TAG" in result
