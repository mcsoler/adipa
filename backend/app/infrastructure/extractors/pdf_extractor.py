import fitz  # PyMuPDF

from app.interfaces.extractors.text_extractor import ITextExtractor


class PdfExtractor(ITextExtractor):
    """Extrae texto de archivos PDF usando PyMuPDF (SRP: solo extrae PDF)."""

    def extract(self, file_bytes: bytes) -> str:
        text_parts: list[str] = []
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text_parts.append(page.get_text("text"))
        return "\n".join(text_parts).strip()
