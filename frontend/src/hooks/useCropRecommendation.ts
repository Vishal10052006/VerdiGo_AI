/**
 * ============================================================================
 * useCropRecommendation Hook
 * ============================================================================
 *
 * Encapsulates crop recommendation fetching, loading, and error
 * state, following the same pattern as useDashboard.
 *
 * Module:
 * Phase 1 → Module 6 → Crop Recommendation
 * ============================================================================
 */

"use client";

import { useEffect, useState } from "react";

import { getCropRecommendations } from "@/services/cropRecommendation.service";
import type { CropRecommendationResponse } from "@/types/cropRecommendation";

interface UseCropRecommendationResult {
  recommendation: CropRecommendationResponse | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useCropRecommendation(
  farmId: string | undefined
): UseCropRecommendationResult {
  const [recommendation, setRecommendation] =
    useState<CropRecommendationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    if (!farmId) {
      setLoading(false);
      return;
    }

    let cancelled = false;

    const fetchRecommendations = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await getCropRecommendations(farmId);

        if (!cancelled) {
          setRecommendation(response);
        }
      } catch (err) {
        console.error("Crop recommendation fetch error:", err);

        if (!cancelled) {
          setError("Unable to load crop recommendations. Please try again.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchRecommendations();

    return () => {
      cancelled = true;
    };
  }, [farmId, refreshKey]);

  const refetch = () => setRefreshKey((key) => key + 1);

  return { recommendation, loading, error, refetch };
}