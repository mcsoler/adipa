interface ProcessingIndicatorProps {
  progress: number;
  label: string;
}

export function ProcessingIndicator({ progress, label }: ProcessingIndicatorProps) {
  return (
    <div className="flex flex-col gap-4 py-8">
      <div className="flex justify-between text-sm text-gray-500 mb-1">
        <span>{label}</span>
        <span>{progress}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
        <div
          className="h-3 rounded-full bg-brand-500 transition-all duration-[1500ms] ease-in-out"
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="text-xs text-gray-400 text-center">
        El modelo de IA puede tardar entre 1 y 3 minutos según el tamaño del documento
      </p>
    </div>
  );
}
