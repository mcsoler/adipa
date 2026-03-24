import { ExtractionResult } from "@/types/extraction";
import { QuestionCard } from "./QuestionCard";
import { DownloadButton } from "./DownloadButton";

interface ExtractionResultViewProps {
  result: ExtractionResult;
  onReset: () => void;
}

export function ExtractionResultView({ result, onReset }: ExtractionResultViewProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Preguntas detectadas</h2>
          <p className="text-sm text-gray-500 mt-1">
            {result.total_preguntas} pregunta{result.total_preguntas !== 1 ? "s" : ""} encontrada
            {result.total_preguntas !== 1 ? "s" : ""}
          </p>
        </div>
        <div className="flex gap-3">
          <DownloadButton result={result} />
          <button
            onClick={onReset}
            className="px-4 py-2 text-sm font-medium text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Nuevo documento
          </button>
        </div>
      </div>

      {result.total_preguntas === 0 ? (
        <div className="text-center py-12 text-gray-400">
          <p className="text-lg">No se detectaron preguntas en el documento.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {result.preguntas.map((q) => (
            <QuestionCard key={q.numero} question={q} />
          ))}
        </div>
      )}
    </div>
  );
}
