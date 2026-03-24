import { useState, useCallback, useRef, useEffect } from "react";
import { uploadDocument } from "@/services/documentService";
import { triggerExtraction } from "@/services/extractionService";
import { ExtractionResult } from "@/types/extraction";

type UploadStatus = "idle" | "uploading" | "processing" | "success" | "error";

interface UseDocumentUploadReturn {
  status: UploadStatus;
  result: ExtractionResult | null;
  error: string | null;
  selectedFile: File | null;
  progress: number;
  progressLabel: string;
  selectFile: (file: File) => void;
  submit: () => Promise<void>;
  reset: () => void;
}

const ACCEPTED_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
];

const PROGRESS_STEPS = [
  { at: 10, label: "Subiendo documento..." },
  { at: 30, label: "Leyendo contenido del archivo..." },
  { at: 55, label: "Enviando texto al modelo de IA..." },
  { at: 80, label: "Generando respuesta con phi..." },
  { at: 92, label: "Validando preguntas extraídas..." },
];

export function useDocumentUpload(): UseDocumentUploadReturn {
  const [status, setStatus] = useState<UploadStatus>("idle");
  const [result, setResult] = useState<ExtractionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);
  const [progressLabel, setProgressLabel] = useState("");
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const clearTimer = () => {
    if (timerRef.current) clearTimeout(timerRef.current);
  };

  useEffect(() => () => clearTimer(), []);

  const animateProgress = useCallback((steps: typeof PROGRESS_STEPS, idx = 0) => {
    if (idx >= steps.length) return;
    const { at, label } = steps[idx];
    setProgress(at);
    setProgressLabel(label);
    timerRef.current = setTimeout(() => animateProgress(steps, idx + 1), 8000);
  }, []);

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
      setProgress(5);
      setProgressLabel("Conectando con el servidor...");

      const uploaded = await uploadDocument(selectedFile);

      setStatus("processing");
      animateProgress(PROGRESS_STEPS);

      const processed = await triggerExtraction(uploaded.document_id, selectedFile);

      clearTimer();

      if (processed.status === "failed") {
        throw new Error(processed.error ?? "Error al procesar el documento.");
      }

      setProgress(100);
      setProgressLabel("¡Listo!");
      setResult(processed.result ?? { total_preguntas: 0, preguntas: [] });
      setStatus("success");
    } catch (err) {
      clearTimer();
      setError(err instanceof Error ? err.message : "Error inesperado.");
      setStatus("error");
    }
  }, [selectedFile, animateProgress]);

  const reset = useCallback(() => {
    clearTimer();
    setStatus("idle");
    setResult(null);
    setError(null);
    setSelectedFile(null);
    setProgress(0);
    setProgressLabel("");
  }, []);

  return { status, result, error, selectedFile, progress, progressLabel, selectFile, submit, reset };
}
