import { ProcessingResponse } from "@/types/extraction";
import apiClient from "./apiClient";

export async function triggerExtraction(
  documentId: string,
  file: File
): Promise<ProcessingResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const { data } = await apiClient.post<ProcessingResponse>(
    `/api/v1/extractions/${documentId}/process`,
    formData,
    { headers: { "Content-Type": "multipart/form-data" } }
  );
  return data;
}

export async function getExtractionResult(
  documentId: string
): Promise<ProcessingResponse> {
  const { data } = await apiClient.get<ProcessingResponse>(
    `/api/v1/extractions/${documentId}`
  );
  return data;
}
