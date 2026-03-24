import { useState, useCallback } from "react";
import { uploadDocument } from "@/services/documentService";
import { triggerExtraction } from "@/services/extractionService";
import { ExtractionResult } from "@/types/extraction";

type UploadStatus = "idle" | "uploading" | "processing" | "success" | "error";

interface UseDocumentUploadReturn {
  status: UploadStatus;
  result: ExtractionResult | null;
  error: string | null;
  selectedFile: File | null;
  selectFile: (file: File) => void;
  submit: () => Promise<void>;
  reset: () => void;
}

const ACCEPTED_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
];

export function useDocumentUpload(): UseDocumentUploadReturn {
  const [status, setStatus] = useState<UploadStatus>("idle");
  const [result, setResult] = useState<ExtractionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const selectFile = useCallback((file: File) => {
    if (!ACCEPTED_TYPES.includes(file.type)) {
      setError("Formato no soportado. Use PDF, DOCX o XLSX.");
      return;
    }
    setSelectedFile(file);
    setError(null);
    setStatus("idle");
  }, []);

  const submit = useCallback(async () => {
    if (!selectedFile) return;

    try {
      setStatus("uploading");
      setError(null);

      const uploaded = await uploadDocument(selectedFile);

      setStatus("processing");
      const processed = await triggerExtraction(uploaded.document_id, selectedFile);

      if (processed.status === "failed") {
        throw new Error(processed.error ?? "Error al procesar el documento.");
      }

      setResult(processed.result ?? { total_preguntas: 0, preguntas: [] });
      setStatus("success");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error inesperado.");
      setStatus("error");
    }
  }, [selectedFile]);

  const reset = useCallback(() => {
    setStatus("idle");
    setResult(null);
    setError(null);
    setSelectedFile(null);
  }, []);

  return { status, result, error, selectedFile, selectFile, submit, reset };
}
