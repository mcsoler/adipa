interface ProcessingIndicatorProps {
  status: "uploading" | "processing";
}

const MESSAGES: Record<string, string> = {
  uploading: "Subiendo documento...",
  processing: "Extrayendo preguntas con IA...",
};

export function ProcessingIndicator({ status }: ProcessingIndicatorProps) {
  return (
    <div className="flex flex-col items-center gap-4 py-10">
      <div className="relative w-14 h-14">
        <div className="absolute inset-0 border-4 border-brand-100 rounded-full" />
        <div className="absolute inset-0 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
      <p className="text-gray-600 font-medium">{MESSAGES[status]}</p>
      <p className="text-sm text-gray-400">Esto puede tardar unos segundos</p>
    </div>
  );
}
