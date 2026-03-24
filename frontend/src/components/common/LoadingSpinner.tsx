interface LoadingSpinnerProps {
  label?: string;
}

export function LoadingSpinner({ label = "Cargando..." }: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center gap-3 py-8">
      <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
      <p className="text-sm text-gray-500">{label}</p>
    </div>
  );
}
