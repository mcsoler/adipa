from fastapi import APIRouter

from app.api.v1.endpoints.documents import router as documents_router
from app.api.v1.endpoints.extractions import router as extractions_router

api_router = APIRouter()
api_router.include_router(documents_router)
api_router.include_router(extractions_router)
