/**
 * ============================================================================
 * Crop Recommendation Page
 * ============================================================================
 *
 * Route: /crop-recommendation
 *
 * Fetches the authenticated farmer's farm, then renders ranked
 * crop recommendations for it.
 *
 * Module:
 * Phase 1 → Module 6 → Crop Recommendation
 * ============================================================================
 */

"use client";

import { useEffect, useState } from "react";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import { PageHeader } from "@/components/common/PageHeader";
import CropRecommendationList from "@/components/crop/CropRecommendationList";
import { LoadingSkeleton } from "@/components/common/LoadingSkeleton";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { getFarm } from "@/services/farm.service";
import { Wheat } from "lucide-react";

export default function CropRecommendationPage() {
  const [farmId, setFarmId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const fetchFarm = async () => {
      setLoading(true);
      setError(null);

      try {
        const farm = await getFarm();

        if (!cancelled) {
          setFarmId(farm.id);
        }
      } catch (err) {
        console.error("Farm fetch error:", err);

        if (!cancelled) {
          // A 404 here means the farmer hasn't registered a farm yet —
          // treat that as an empty state, not a hard error.
          setFarmId(null);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchFarm();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <ProtectedRoute>
      <main className="min-h-screen bg-slate-50">
        <PageHeader
          title="Crop Recommendations"
          description="AI-powered suggestions based on your farm's soil, season, and location."
          icon={<Wheat className="h-6 w-6" />}
        />

        <div className="mx-auto max-w-[1600px] px-4 py-6 sm:px-6 lg:px-8">
          {loading ? (
            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {[...Array(3)].map((_, index) => (
                <LoadingSkeleton key={index} variant="card" />
              ))}
            </div>
          ) : error ? (
            <ErrorState
              title="Unable to load your farm"
              description={error}
              actionLabel="Retry"
              onAction={() => window.location.reload()}
            />
          ) : farmId ? (
            <CropRecommendationList farmId={farmId} />
          ) : (
            <EmptyState
              title="No farm registered yet"
              description="Register a farm to get personalized crop recommendations."
              icon={<Wheat className="h-10 w-10" />}
            />
          )}
        </div>
      </main>
    </ProtectedRoute>
  );
}