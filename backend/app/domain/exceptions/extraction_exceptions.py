class NoQuestionsFoundError(Exception):
    def __init__(self):
        super().__init__("No se detectaron preguntas en el documento.")


class LLMUnavailableError(Exception):
    def __init__(self, detail: str = ""):
        super().__init__(f"El servicio LLM no está disponible. {detail}".strip())


class ExtractionTimeoutError(Exception):
    def __init__(self):
        super().__init__("El procesamiento del documento excedió el tiempo límite.")
