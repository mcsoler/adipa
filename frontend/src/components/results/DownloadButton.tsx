import { ExtractionResult } from "@/types/extraction";

interface DownloadButtonProps {
  result: ExtractionResult;
  filename?: string;
}

export function DownloadButton({ result, filename = "preguntas.json" }: DownloadButtonProps) {
  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <button
      onClick={handleDownload}
      className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-brand-600 border border-brand-600 rounded-lg hover:bg-brand-50 transition-colors"
    >
      ⬇ Descargar JSON
    </button>
  );
}
