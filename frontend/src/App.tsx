import { useDocumentUpload } from "@/hooks/useDocumentUpload";
import { FileDropzone } from "@/components/upload/FileDropzone";
import { FilePreview } from "@/components/upload/FilePreview";
import { UploadButton } from "@/components/upload/UploadButton";
import { ExtractionResultView } from "@/components/results/ExtractionResultView";
import { ProcessingIndicator } from "@/components/status/ProcessingIndicator";
import { ErrorMessage } from "@/components/status/ErrorMessage";
import { Card } from "@/components/common/Card";

export default function App() {
  const { status, result, error, selectedFile, selectFile, submit, reset } =
    useDocumentUpload();

  const isProcessing = status === "uploading" || status === "processing";

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex flex-col">
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-brand-700">
            ADIPA — Extractor de Preguntas
          </h1>
          <p className="text-sm text-gray-500 mt-0.5">
            Sube un documento y detecta preguntas automáticamente con IA
          </p>
        </div>
      </header>

      <main className="flex-1 max-w-4xl mx-auto w-full px-6 py-10 space-y-6">
        {status !== "success" && (
          <Card>
            <h2 className="text-lg font-semibold text-gray-700 mb-4">
              Cargar documento
            </h2>

            {!selectedFile ? (
              <FileDropzone onFileSelect={selectFile} disabled={isProcessing} />
            ) : (
              <FilePreview file={selectedFile} onRemove={reset} />
            )}

            {error && (
              <div className="mt-4">
                <ErrorMessage message={error} onRetry={reset} />
              </div>
            )}

            {isProcessing ? (
              <ProcessingIndicator status={status as "uploading" | "processing"} />
            ) : (
              <div className="mt-4">
                <UploadButton
                  onClick={submit}
                  isLoading={false}
                  disabled={!selectedFile || isProcessing}
                  label="Extraer preguntas"
                />
              </div>
            )}
          </Card>
        )}

        {status === "success" && result && (
          <Card>
            <ExtractionResultView result={result} onReset={reset} />
          </Card>
        )}
      </main>

      <footer className="py-4 text-center text-xs text-gray-400">
        ADIPA v1.0.0 — Powered by LangGraph + Ollama
      </footer>
    </div>
  );
}
