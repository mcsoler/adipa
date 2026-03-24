from enum import Enum


class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"

    @classmethod
    def from_mime(cls, mime_type: str) -> "FileType":
        mapping = {
            "application/pdf": cls.PDF,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": cls.DOCX,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": cls.XLSX,
        }
        if mime_type not in mapping:
            raise ValueError(f"Tipo MIME no soportado: {mime_type}")
        return mapping[mime_type]

    @classmethod
    def from_extension(cls, filename: str) -> "FileType":
        ext = filename.rsplit(".", 1)[-1].lower()
        mapping = {"pdf": cls.PDF, "docx": cls.DOCX, "xlsx": cls.XLSX}
        if ext not in mapping:
            raise ValueError(f"Extensión no soportada: {ext}")
        return mapping[ext]
