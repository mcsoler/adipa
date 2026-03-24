import { Pregunta } from "@/types/question";
import { Badge } from "@/components/common/Badge";
import { AlternativasList } from "./AlternativasList";

interface QuestionCardProps {
  question: Pregunta;
}

export function QuestionCard({ question }: QuestionCardProps) {
  return (
    <div className="border border-gray-200 rounded-xl p-5 hover:shadow-sm transition-shadow">
      <div className="flex items-start justify-between gap-3 mb-3">
        <span className="text-sm font-bold text-gray-400">#{question.numero}</span>
        <Badge type={question.tipo} />
      </div>

      <p className="text-gray-800 font-medium leading-relaxed">{question.enunciado}</p>

      <AlternativasList
        alternativas={question.alternativas}
        correctAnswer={question.respuesta_correcta}
      />

      {question.tipo === "verdadero_falso" && question.respuesta_correcta && (
        <p className="mt-3 text-sm text-green-700 font-medium bg-green-50 px-3 py-1.5 rounded-lg inline-block">
          ✓ {question.respuesta_correcta}
        </p>
      )}

      {question.tipo === "desarrollo" && (
        <p className="mt-3 text-sm text-gray-400 italic">Respuesta de desarrollo</p>
      )}
    </div>
  );
}
