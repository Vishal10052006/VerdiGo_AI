/**
 * ============================================================================
 * Crop Recommendation List
 * ============================================================================
 *
 * Fetches and renders ranked crop recommendations for a farm,
 * with loading, error, and empty states.
 *
 * Module:
 * Phase 1 → Module 6 → Crop Recommendation
 * ============================================================================
 */

"use client";

import { Sprout } from "lucide-react";

import { useCropRecommendation } from "@/hooks/useCropRecommendation";
import CropRecommendationCard from "./CropRecommendationCard";
import { LoadingSkeleton } from "@/components/common/LoadingSkeleton";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";

interface CropRecommendationListProps {
  farmId: string;
}

export default function CropRecommendationList({
  farmId,
}: CropRecommendationListProps) {
  const { recommendation, loading, error, refetch } =
    useCropRecommendation(farmId);

  if (loading) {
    return (
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {[...Array(3)].map((_, index) => (
          <LoadingSkeleton key={index} variant="card" />
        ))}
      </div>
    );
  }

  if (error || !recommendation) {
    return (
      <ErrorState
        title="Unable to load recommendations"
        description={error ?? "Something went wrong. Please try again."}
        actionLabel="Retry"
        onAction={refetch}
      />
    );
  }

  if (recommendation.items.length === 0) {
    return (
      <EmptyState
        title="No recommendations yet"
        description="We couldn't generate crop recommendations for this farm. Try updating your farm's soil type or location."
        icon={<Sprout className="h-10 w-10" />}
      />
    );
  }

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <p className="text-sm text-slate-500">
          Season:{" "}
          <span className="font-semibold capitalize text-slate-700">
            {recommendation.season}
          </span>
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {recommendation.items.map((item) => (
          <CropRecommendationCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}