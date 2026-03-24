from typing import Any, Optional
from typing_extensions import TypedDict


class WorkflowState(TypedDict):
    """Estado compartido del grafo LangGraph."""
    file_bytes: bytes
    file_type: str
    raw_text: str
    llm_result: dict[str, Any]
    validated_result: dict[str, Any]
    error: Optional[str]
    retry_count: int
