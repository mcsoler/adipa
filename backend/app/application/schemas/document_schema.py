from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    file_type: str
    status: str
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class DocumentUploadResponse(BaseModel):
    document_id: UUID
    filename: str
    status: str
    message: str


class ProcessingResponse(BaseModel):
    document_id: UUID
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None
