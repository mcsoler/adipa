from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.document_exceptions import (
    EmptyDocumentError,
    FileTooLargeError,
    UnsupportedFileTypeError,
)
from app.domain.exceptions.extraction_exceptions import (
    LLMUnavailableError,
    NoQuestionsFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UnsupportedFileTypeError)
    async def handle_unsupported_type(_: Request, exc: UnsupportedFileTypeError):
        return JSONResponse(status_code=415, content={"detail": str(exc)})

    @app.exception_handler(FileTooLargeError)
    async def handle_file_too_large(_: Request, exc: FileTooLargeError):
        return JSONResponse(status_code=413, content={"detail": str(exc)})

    @app.exception_handler(EmptyDocumentError)
    async def handle_empty_document(_: Request, exc: EmptyDocumentError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(NoQuestionsFoundError)
    async def handle_no_questions(_: Request, exc: NoQuestionsFoundError):
        return JSONResponse(status_code=200, content={
            "detail": str(exc),
            "total_preguntas": 0,
            "preguntas": [],
        })

    @app.exception_handler(LLMUnavailableError)
    async def handle_llm_unavailable(_: Request, exc: LLMUnavailableError):
        return JSONResponse(status_code=503, content={"detail": str(exc)})
