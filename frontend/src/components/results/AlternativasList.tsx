import { Alternativa } from "@/types/question";

interface AlternativasListProps {
  alternativas: Alternativa[];
  correctAnswer: string | null;
}

export function AlternativasList({ alternativas, correctAnswer }: AlternativasListProps) {
  if (alternativas.length === 0) return null;

  return (
    <ul className="mt-3 space-y-1.5">
      {alternativas.map((alt) => {
        const isCorrect = correctAnswer === alt.letra;
        return (
          <li
            key={alt.letra}
            className={`flex items-start gap-2 text-sm px-3 py-2 rounded-lg ${
              isCorrect
                ? "bg-green-50 border border-green-200 text-green-800 font-medium"
                : "bg-gray-50 text-gray-700"
            }`}
          >
            <span className="font-bold min-w-[1.25rem]">{alt.letra}.</span>
            <span>{alt.texto}</span>
            {isCorrect && <span className="ml-auto text-green-600 text-xs">✓ Correcta</span>}
          </li>
        );
      })}
    </ul>
  );
}
