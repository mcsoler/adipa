import io

from docx import Document

from app.interfaces.extractors.text_extractor import ITextExtractor


class DocxExtractor(ITextExtractor):
    """Extrae texto de archivos DOCX usando python-docx (SRP: solo extrae DOCX)."""

    def extract(self, file_bytes: bytes) -> str:
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs).strip()
