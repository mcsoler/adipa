from uuid import UUID

from app.application.schemas.document_schema import ProcessingResponse
from app.domain.exceptions.extraction_exceptions import NoQuestionsFoundError
from app.interfaces.repositories.document_repository import IDocumentRepository
from app.interfaces.repositories.extraction_repository import IExtractionRepository
from app.langgraph_workflow.graph import extraction_graph
from app.langgraph_workflow.state import WorkflowState


class ExtractQuestionsUseCase:
    """Caso de uso: ejecutar el pipeline LangGraph y persistir el resultado (SRP)."""

    def __init__(
        self,
        document_repo: IDocumentRepository,
        extraction_repo: IExtractionRepository,
    ):
        self._doc_repo = document_repo
        self._ext_repo = extraction_repo

    async def execute(self, document_id: UUID, file_bytes: bytes, file_type: str) -> ProcessingResponse:
        await self._doc_repo.update_status(document_id, "processing")

        initial_state: WorkflowState = {
            "file_bytes": file_bytes,
            "file_type": file_type,
            "raw_text": "",
            "llm_result": {},
            "validated_result": {},
            "error": None,
            "retry_count": 0,
        }

        final_state = extraction_graph.invoke(initial_state, {"recursion_limit": 10})

        if final_state.get("error"):
            await self._doc_repo.update_status(document_id, "failed")
            return ProcessingResponse(
                document_id=document_id,
                status="failed",
                error=final_state["error"],
            )

        result = final_state["validated_result"]

        if result.get("total_preguntas", 0) == 0:
            await self._doc_repo.update_status(document_id, "completed")
            await self._ext_repo.save(document_id, result)
            raise NoQuestionsFoundError()

        await self._ext_repo.save(document_id, result)
        await self._doc_repo.update_status(document_id, "completed")

        return ProcessingResponse(
            document_id=document_id,
            status="completed",
            result=result,
        )
