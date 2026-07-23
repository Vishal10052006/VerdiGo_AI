export type DiseaseSeverity = "none" | "low" | "moderate" | "high" | "critical";

export interface DiseaseDetection {
  id: string;
  farm_id: string;
  image_url: string;
  crop_type: string | null;
  is_healthy: boolean;
  disease_name: string | null;
  confidence: number;
  severity: DiseaseSeverity;
  treatment: string[];
  prevention_tips: string[];
  ai_provider: string;
  created_at: string;
}

export interface DiseaseHistoryResponse {
  farm_id: string;
  detections: DiseaseDetection[];
}