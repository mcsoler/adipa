import { DocumentUploadResponse } from "@/types/extraction";
import apiClient from "./apiClient";

export async function uploadDocument(file: File): Promise<DocumentUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const { data } = await apiClient.post<DocumentUploadResponse>(
    "/api/v1/documents/upload",
    formData,
    { headers: { "Content-Type": "multipart/form-data" } }
  );
  return data;
}
