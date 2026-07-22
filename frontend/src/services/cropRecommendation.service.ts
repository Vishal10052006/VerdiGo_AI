/**
 * ============================================================================
 * Crop Recommendation Service
 * ============================================================================
 *
 * Handles all Crop Recommendation API requests.
 *
 * Module:
 * Phase 1 → Module 6 → Crop Recommendation
 * ============================================================================
 */

import api from "@/lib/api";
import type { CropRecommendationResponse } from "@/types/cropRecommendation";

/**
 * ============================================================================
 * Get Crop Recommendations
 * ============================================================================
 *
 * Generates and returns ranked crop recommendations for a farm.
 */
export const getCropRecommendations = async (
  farmId: string
): Promise<CropRecommendationResponse> => {
  const response = await api.get(`/v1/crop-recommendation/${farmId}`);
  return response.data.data;
};

/**
 * ============================================================================
 * Get Recommendation Details
 * ============================================================================
 */
export const getRecommendationDetails = async (
  recommendationId: string
): Promise<CropRecommendationResponse> => {
  const response = await api.get(
    `/v1/crop-recommendation/details/${recommendationId}`
  );
  return response.data.data;
};