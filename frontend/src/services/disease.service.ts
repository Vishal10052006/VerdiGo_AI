import api from "@/lib/api";
import type { DiseaseDetection, DiseaseHistoryResponse } from "@/types/disease";

export const detectDisease = async (
  farmId: string,
  file: File,
  cropType?: string
): Promise<DiseaseDetection> => {
  const formData = new FormData();
  formData.append("file", file);
  if (cropType) formData.append("crop_type", cropType);

  const response = await api.post(`/v1/disease/detect/${farmId}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data.data;
};

export const getDiseaseHistory = async (
  farmId: string
): Promise<DiseaseHistoryResponse> => {
  const response = await api.get(`/v1/disease/history/${farmId}`);
  return response.data.data;
};