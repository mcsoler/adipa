import { Pregunta } from "./question";

export interface ExtractionResult {
  total_preguntas: number;
  preguntas: Pregunta[];
}

export interface ProcessingResponse {
  document_id: string;
  status: "pending" | "processing" | "completed" | "failed" | "not_found";
  result?: ExtractionResult;
  error?: string;
}

export interface DocumentUploadResponse {
  document_id: string;
  filename: string;
  status: string;
  message: string;
}
