/**
 * TDD - RED PHASE
 * Tests del componente FileDropzone escritos antes de verificar comportamiento completo.
 */
import { render, screen } from "@testing-library/react";
import { vi, describe, it, expect } from "vitest";
import { FileDropzone } from "./FileDropzone";

describe("FileDropzone", () => {
  // RED 1: renderiza instrucciones de drag-and-drop
  it("renders drag and drop instructions", () => {
    render(<FileDropzone onFileSelect={vi.fn()} />);
    expect(screen.getByText(/arrastra un archivo/i)).toBeDefined();
  });

  // RED 2: muestra formatos aceptados
  it("shows accepted file formats", () => {
    render(<FileDropzone onFileSelect={vi.fn()} />);
    expect(screen.getByText(/PDF, DOCX o XLSX/i)).toBeDefined();
  });

  // RED 3: cuando está deshabilitado aplica estilos de opacidad
  it("applies disabled styles when disabled prop is true", () => {
    const { container } = render(
      <FileDropzone onFileSelect={vi.fn()} disabled={true} />
    );
    const dropzone = container.firstChild as HTMLElement;
    expect(dropzone.className).toContain("opacity-50");
  });

  // RED 4: tiene input de archivo accesible
  it("renders a file input element", () => {
    render(<FileDropzone onFileSelect={vi.fn()} />);
    expect(screen.getByTestId("file-input")).toBeDefined();
  });
});
