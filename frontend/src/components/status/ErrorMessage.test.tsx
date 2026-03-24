import { render, screen, fireEvent } from "@testing-library/react";
import { vi, describe, it, expect } from "vitest";
import { ErrorMessage } from "./ErrorMessage";

describe("ErrorMessage", () => {
  it("renders error message", () => {
    render(<ErrorMessage message="Archivo no válido" />);
    expect(screen.getByText("Archivo no válido")).toBeDefined();
  });

  it("calls onRetry when button is clicked", () => {
    const onRetry = vi.fn();
    render(<ErrorMessage message="Error" onRetry={onRetry} />);
    fireEvent.click(screen.getByText("Intentar de nuevo"));
    expect(onRetry).toHaveBeenCalledOnce();
  });

  it("does not render retry button without onRetry prop", () => {
    render(<ErrorMessage message="Error" />);
    expect(screen.queryByText("Intentar de nuevo")).toBeNull();
  });
});
