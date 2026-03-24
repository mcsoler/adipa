interface FilePreviewProps {
  file: File;
  onRemove: () => void;
}

const ICONS: Record<string, string> = {
  pdf: "📄",
  docx: "📝",
  xlsx: "📊",
};

export function FilePreview({ file, onRemove }: FilePreviewProps) {
  const ext = file.name.split(".").pop()?.toLowerCase() ?? "";
  const sizeMB = (file.size / (1024 * 1024)).toFixed(2);

  return (
    <div className="flex items-center justify-between bg-gray-50 rounded-lg px-4 py-3 border border-gray-200">
      <div className="flex items-center gap-3">
        <span className="text-2xl">{ICONS[ext] ?? "📁"}</span>
        <div>
          <p className="text-sm font-medium text-gray-800 truncate max-w-xs">{file.name}</p>
          <p className="text-xs text-gray-500">{sizeMB} MB</p>
        </div>
      </div>
      <button
        onClick={onRemove}
        className="text-gray-400 hover:text-red-500 transition-colors"
        aria-label="Eliminar archivo"
      >
        ✕
      </button>
    </div>
  );
}
