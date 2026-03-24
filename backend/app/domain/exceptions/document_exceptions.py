class UnsupportedFileTypeError(Exception):
    def __init__(self, file_type: str):
        super().__init__(f"Tipo de archivo no soportado: {file_type}. Use PDF, DOCX o XLSX.")
        self.file_type = file_type


class FileTooLargeError(Exception):
    def __init__(self, size_mb: float, max_mb: int):
        super().__init__(f"Archivo demasiado grande: {size_mb:.1f}MB. Máximo: {max_mb}MB.")
        self.size_mb = size_mb
        self.max_mb = max_mb


class EmptyDocumentError(Exception):
    def __init__(self):
        super().__init__("El documento está vacío o no contiene texto extraíble.")
