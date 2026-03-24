import { QuestionType } from "@/types/question";

interface BadgeProps {
  type: QuestionType;
}

const TYPE_LABELS: Record<QuestionType, string> = {
  seleccion_multiple: "Selección múltiple",
  verdadero_falso: "Verdadero / Falso",
  desarrollo: "Desarrollo",
  emparejamiento: "Emparejamiento",
};

const TYPE_COLORS: Record<QuestionType, string> = {
  seleccion_multiple: "bg-blue-100 text-blue-700",
  verdadero_falso: "bg-green-100 text-green-700",
  desarrollo: "bg-purple-100 text-purple-700",
  emparejamiento: "bg-orange-100 text-orange-700",
};

export function Badge({ type }: BadgeProps) {
  return (
    <span
      className={`inline-block text-xs font-semibold px-2 py-0.5 rounded-full ${TYPE_COLORS[type]}`}
    >
      {TYPE_LABELS[type]}
    </span>
  );
}
