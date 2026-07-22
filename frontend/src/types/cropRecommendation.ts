/**
 * ============================================================================
 * Crop Recommendation Types
 * ============================================================================
 *
 * Mirrors the backend's CropRecommendationResponseSchema.
 *
 * Module:
 * Phase 1 → Module 6 → Crop Recommendation
 * ============================================================================
 */

export interface CropReasoning {
  soil: string;
  season: string;
  location: string;
}

export interface CropSummary {
  id: string;
  name: string;
  water_requirement: "low" | "medium" | "high";
  growth_duration_days: number;
  expected_yield_per_acre: string | null;
}

export interface CropRecommendationItem {
  id: string;
  rank: number;
  score: number;
  crop: CropSummary;
  reasoning: CropReasoning;
}

export interface CropRecommendationResponse {
  id: string;
  farm_id: string;
  season: "kharif" | "rabi" | "zaid";
  source: string;
  generated_at: string;
  items: CropRecommendationItem[];
}