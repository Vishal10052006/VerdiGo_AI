"use client";

import { useState } from "react";
import { detectDisease } from "@/services/disease.service";
import type { DiseaseDetection } from "@/types/disease";

interface UseDiseaseDetectionResult {
  result: DiseaseDetection | null;
  analyzing: boolean;
  error: string | null;
  analyze: (farmId: string, file: File, cropType?: string) => Promise<void>;
  reset: () => void;
}

export function useDiseaseDetection(): UseDiseaseDetectionResult {
  const [result, setResult] = useState<DiseaseDetection | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyze = async (farmId: string, file: File, cropType?: string) => {
    setAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const detection = await detectDisease(farmId, file, cropType);
      setResult(detection);
    } catch (err: any) {
      const status = err?.response?.status;
      if (status === 503 || status === 502) {
        setError("AI Vision is temporarily unavailable. Please try again shortly.");
      } else if (status === 400) {
        setError(err?.response?.data?.detail ?? "Invalid image. Please try another photo.");
      } else {
        setError("Unable to analyze image. Please try again.");
      }
    } finally {
      setAnalyzing(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
  };

  return { result, analyzing, error, analyze, reset };
}