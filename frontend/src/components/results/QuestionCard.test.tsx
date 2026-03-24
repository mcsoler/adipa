import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { QuestionCard } from "./QuestionCard";
import { Pregunta } from "@/types/question";

const multipleChoice: Pregunta = {
  numero: 1,
  enunciado: "¿Cuál es el principal criterio del TAG?",
  tipo: "seleccion_multiple",
  alternativas: [
    { letra: "A", texto: "Alucinaciones visuales" },
    { letra: "B", texto: "Preocupación excesiva" },
  ],
  respuesta_correcta: "B",
};

const trueFalse: Pregunta = {
  numero: 2,
  enunciado: "La TCC es efectiva para el TAG.",
  tipo: "verdadero_falso",
  alternativas: [],
  respuesta_correcta: "Verdadero",
};

describe("QuestionCard", () => {
  it("renders question number and text", () => {
    render(<QuestionCard question={multipleChoice} />);
    expect(screen.getByText("#1")).toBeDefined();
    expect(screen.getByText("¿Cuál es el principal criterio del TAG?")).toBeDefined();
  });

  it("renders alternatives for multiple choice", () => {
    render(<QuestionCard question={multipleChoice} />);
    expect(screen.getByText("Alucinaciones visuales")).toBeDefined();
    expect(screen.getByText("Preocupación excesiva")).toBeDefined();
  });

  it("highlights correct answer", () => {
    render(<QuestionCard question={multipleChoice} />);
    expect(screen.getByText("✓ Correcta")).toBeDefined();
  });

  it("renders true/false answer", () => {
    render(<QuestionCard question={trueFalse} />);
    expect(screen.getByText(/Verdadero/)).toBeDefined();
  });
});
