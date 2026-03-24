from app.domain.exceptions.document_exceptions import EmptyDocumentError, UnsupportedFileTypeError
from app.domain.value_objects.file_type import FileType
from app.infrastructure.extractors.extractor_factory import ExtractorFactory
from app.langgraph_workflow.state import WorkflowState


def extract_text_node(state: WorkflowState) -> WorkflowState:
    """Nodo 1: extrae texto del archivo usando el extractor correspondiente (SRP)."""
    try:
        file_type = FileType(state["file_type"])
        extractor = ExtractorFactory.get(file_type)
        raw_text = extractor.extract(state["file_bytes"])

        if not raw_text.strip():
            raise EmptyDocumentError()

        return {**state, "raw_text": raw_text, "error": None}

    except (UnsupportedFileTypeError, EmptyDocumentError) as exc:
        return {**state, "raw_text": "", "error": str(exc)}
    except Exception as exc:
        return {**state, "raw_text": "", "error": f"Error extrayendo texto: {exc}"}
