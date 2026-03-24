import { renderHook, act } from "@testing-library/react";
import { vi, describe, it, expect, beforeEach } from "vitest";
import { useDocumentUpload } from "./useDocumentUpload";

vi.mock("@/services/documentService", () => ({
  uploadDocument: vi.fn(),
}));

vi.mock("@/services/extractionService", () => ({
  triggerExtraction: vi.fn(),
}));

const { uploadDocument } = await import("@/services/documentService");
const { triggerExtraction } = await import("@/services/extractionService");

const makePdfFile = () =>
  new File(["content"], "test.pdf", { type: "application/pdf" });

const makeUnsupportedFile = () =>
  new File(["content"], "test.pptx", { type: "application/vnd.ms-powerpoint" });

describe("useDocumentUpload", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("starts with idle status", () => {
    const { result } = renderHook(() => useDocumentUpload());
    expect(result.current.status).toBe("idle");
  });

  it("selects a valid file", () => {
    const { result } = renderHook(() => useDocumentUpload());
    act(() => result.current.selectFile(makePdfFile()));
    expect(result.current.selectedFile?.name).toBe("test.pdf");
    expect(result.current.error).toBeNull();
  });

  it("rejects unsupported file type", () => {
    const { result } = renderHook(() => useDocumentUpload());
    act(() => result.current.selectFile(makeUnsupportedFile()));
    expect(result.current.selectedFile).toBeNull();
    expect(result.current.error).toContain("Formato no soportado");
  });

  it("resets to initial state", () => {
    const { result } = renderHook(() => useDocumentUpload());
    act(() => result.current.selectFile(makePdfFile()));
    act(() => result.current.reset());
    expect(result.current.status).toBe("idle");
    expect(result.current.selectedFile).toBeNull();
  });

  it("completes full upload and extraction flow", async () => {
    (uploadDocument as ReturnType<typeof vi.fn>).mockResolvedValue({
      document_id: "abc-123",
      filename: "test.pdf",
      status: "pending",
      message: "OK",
    });

    (triggerExtraction as ReturnType<typeof vi.fn>).mockResolvedValue({
      document_id: "abc-123",
      status: "completed",
      result: { total_preguntas: 1, preguntas: [] },
    });

    const { result } = renderHook(() => useDocumentUpload());
    act(() => result.current.selectFile(makePdfFile()));
    await act(() => result.current.submit());

    expect(result.current.status).toBe("success");
    expect(result.current.result?.total_preguntas).toBe(1);
  });

  it("sets error status on failure", async () => {
    (uploadDocument as ReturnType<typeof vi.fn>).mockRejectedValue(
      new Error("Servidor no disponible")
    );

    const { result } = renderHook(() => useDocumentUpload());
    act(() => result.current.selectFile(makePdfFile()));
    await act(() => result.current.submit());

    expect(result.current.status).toBe("error");
    expect(result.current.error).toContain("Servidor no disponible");
  });
});
