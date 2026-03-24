/**
 * TDD - RED PHASE
 * Tests de la vista de resultados completa.
 */
import { render, screen, fireEvent } from "@testing-library/react";
import { vi, describe, it, expect } from "vitest";
import { ExtractionResultView } from "./ExtractionResultView";
import { ExtractionResult } from "@/types/extraction";

const mockResult: ExtractionResult = {
  total_preguntas: 2,
  preguntas: [
    {
      numero: 1,
      enunciado: "¿Qué es el TAG?",
      tipo: "seleccion_multiple",
      alternativas: [{ letra: "A", texto: "Trastorno de ansiedad" }],
      respuesta_correcta: "A",
    },
    {
      numero: 2,
      enunciado: "La TCC es efectiva para el TAG.",
      tipo: "verdadero_falso",
      alternativas: [],
      respuesta_correcta: "Verdadero",
    },
  ],
};

const emptyResult: ExtractionResult = { total_preguntas: 0, preguntas: [] };

describe("ExtractionResultView", () => {
  // RED 1: muestra el total de preguntas
  it("displays total questions count", () => {
    render(<ExtractionResultView result={mockResult} onReset={vi.fn()} />);
    expect(screen.getByText(/2 preguntas encontradas/i)).toBeDefined();
  });

  // RED 2: renderiza cada QuestionCard
  it("renders all question cards", () => {
    render(<ExtractionResultView result={mockResult} onReset={vi.fn()} />);
    expect(screen.getByText("¿Qué es el TAG?")).toBeDefined();
    expect(screen.getByText("La TCC es efectiva para el TAG.")).toBeDefined();
  });

  // RED 3: sin preguntas muestra mensaje vacío
  it("shows empty message when no questions found", () => {
    render(<ExtractionResultView result={emptyResult} onReset={vi.fn()} />);
    expect(screen.getByText(/no se detectaron preguntas/i)).toBeDefined();
  });

  // RED 4: botón "Nuevo documento" llama a onReset
  it("calls onReset when new document button is clicked", () => {
    const onReset = vi.fn();
    render(<ExtractionResultView result={mockResult} onReset={onReset} />);
    fireEvent.click(screen.getByText(/nuevo documento/i));
    expect(onReset).toHaveBeenCalledOnce();
  });
});
