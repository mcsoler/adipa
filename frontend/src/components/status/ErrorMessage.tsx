interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3">
      <span className="text-red-500 text-xl mt-0.5">⚠</span>
      <div className="flex-1">
        <p className="text-sm text-red-700 font-medium">{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="mt-2 text-sm text-red-600 underline hover:no-underline"
          >
            Intentar de nuevo
          </button>
        )}
      </div>
    </div>
  );
}
