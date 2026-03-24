from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.extract_questions import ExtractQuestionsUseCase
from app.application.use_cases.get_extraction_result import GetExtractionResultUseCase
from app.application.use_cases.upload_document import UploadDocumentUseCase
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.postgres_document_repository import PostgresDocumentRepository
from app.infrastructure.repositories.postgres_extraction_repository import PostgresExtractionRepository


def get_document_repo(db: AsyncSession = Depends(get_db)) -> PostgresDocumentRepository:
    return PostgresDocumentRepository(db)


def get_extraction_repo(db: AsyncSession = Depends(get_db)) -> PostgresExtractionRepository:
    return PostgresExtractionRepository(db)


def get_upload_use_case(
    doc_repo: PostgresDocumentRepository = Depends(get_document_repo),
) -> UploadDocumentUseCase:
    return UploadDocumentUseCase(doc_repo)


def get_extract_use_case(
    doc_repo: PostgresDocumentRepository = Depends(get_document_repo),
    ext_repo: PostgresExtractionRepository = Depends(get_extraction_repo),
) -> ExtractQuestionsUseCase:
    return ExtractQuestionsUseCase(doc_repo, ext_repo)


def get_result_use_case(
    doc_repo: PostgresDocumentRepository = Depends(get_document_repo),
    ext_repo: PostgresExtractionRepository = Depends(get_extraction_repo),
) -> GetExtractionResultUseCase:
    return GetExtractionResultUseCase(doc_repo, ext_repo)
