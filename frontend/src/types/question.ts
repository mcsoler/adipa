export type QuestionType =
  | "seleccion_multiple"
  | "verdadero_falso"
  | "desarrollo"
  | "emparejamiento";

export interface Alternativa {
  letra: string;
  texto: string;
}

export interface Pregunta {
  numero: number;
  enunciado: string;
  tipo: QuestionType;
  alternativas: Alternativa[];
  respuesta_correcta: string | null;
}
