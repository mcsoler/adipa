/**
 * TDD - RED PHASE
 * Tests del botón de descarga de JSON.
 */
import { render, screen, fireEvent } from "@testing-library/react";
import { vi, describe, it, expect, beforeEach, afterEach } from "vitest";
import { DownloadButton } from "./DownloadButton";
import { ExtractionResult } from "@/types/extraction";

const mockResult: ExtractionResult = {
  total_preguntas: 1,
  preguntas: [{
    numero: 1,
    enunciado: "¿Qué es el TAG?",
    tipo: "seleccion_multiple",
    alternativas: [{ letra: "A", texto: "Ansiedad" }],
    respuesta_correcta: "A",
  }],
};

describe("DownloadButton", () => {
  let createObjectURLMock: ReturnType<typeof vi.fn>;
  let revokeObjectURLMock: ReturnType<typeof vi.fn>;
  let anchorClickMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    createObjectURLMock = vi.fn().mockReturnValue("blob:mock-url");
    revokeObjectURLMock = vi.fn();
    anchorClickMock = vi.fn();

    global.URL.createObjectURL = createObjectURLMock;
    global.URL.revokeObjectURL = revokeObjectURLMock;

    vi.spyOn(document, "createElement").mockImplementation((tag: string) => {
      if (tag === "a") {
        return { href: "", download: "", click: anchorClickMock } as unknown as HTMLElement;
      }
      return document.createElement(tag);
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // RED 1: renderiza el botón con texto correcto
  it("renders download button with correct label", () => {
    render(<DownloadButton result={mockResult} />);
    expect(screen.getByText(/descargar json/i)).toBeDefined();
  });

  // RED 2: al hacer click crea un Blob y dispara descarga
  it("triggers file download on click", () => {
    render(<DownloadButton result={mockResult} />);
    fireEvent.click(screen.getByText(/descargar json/i));

    expect(createObjectURLMock).toHaveBeenCalledOnce();
    expect(anchorClickMock).toHaveBeenCalledOnce();
    expect(revokeObjectURLMock).toHaveBeenCalledOnce();
  });

  // RED 3: el archivo descargado tiene el nombre correcto
  it("uses provided filename for download", () => {
    const mockAnchor = { href: "", download: "", click: anchorClickMock } as unknown as HTMLAnchorElement;
    vi.spyOn(document, "createElement").mockReturnValue(mockAnchor);

    render(<DownloadButton result={mockResult} filename="mis_preguntas.json" />);
    fireEvent.click(screen.getByText(/descargar json/i));

    expect(mockAnchor.download).toBe("mis_preguntas.json");
  });
});
