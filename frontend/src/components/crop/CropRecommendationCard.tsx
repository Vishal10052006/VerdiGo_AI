/**
 * ============================================================================
 * Crop Recommendation Card
 * ============================================================================
 *
 * Displays a single ranked crop suggestion with score, water
 * requirement, and the reasoning behind the match.
 *
 * Module:
 * Phase 1 → Module 6 → Crop Recommendation
 * ============================================================================
 */

import {
  Wheat,
  Droplets,
  CalendarDays,
  TrendingUp,
} from "lucide-react";

import type { CropRecommendationItem } from "@/types/cropRecommendation";

interface CropRecommendationCardProps {
  item: CropRecommendationItem;
}

const WATER_STYLES: Record<string, string> = {
  low: "bg-emerald-100 text-emerald-700",
  medium: "bg-amber-100 text-amber-700",
  high: "bg-blue-100 text-blue-700",
};

export default function CropRecommendationCard({
  item,
}: CropRecommendationCardProps) {
  const { rank, score, crop, reasoning } = item;

  return (
    <div
      className="
        rounded-2xl
        border
        border-slate-200
        bg-white
        p-6
        shadow-sm
        transition-all
        duration-300
        hover:-translate-y-1
        hover:shadow-md
      "
    >
      {/* Header */}
      <div className="mb-4 flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-green-100">
            <Wheat className="h-6 w-6 text-green-600" />
          </div>

          <div>
            <p className="text-xs font-medium text-slate-400">
              #{rank} Recommended
            </p>
            <h3 className="text-lg font-bold text-slate-900">
              {crop.name}
            </h3>
          </div>
        </div>

        <span className="rounded-full bg-emerald-50 px-3 py-1 text-sm font-semibold text-emerald-700">
          {Math.round(score)}% match
        </span>
      </div>

      {/* Stats */}
      <div className="mb-4 flex flex-wrap gap-3 text-sm">
        <span
          className={`flex items-center gap-1 rounded-full px-3 py-1 font-medium ${
            WATER_STYLES[crop.water_requirement] ?? "bg-slate-100 text-slate-600"
          }`}
        >
          <Droplets className="h-3.5 w-3.5" />
          {crop.water_requirement} water
        </span>

        <span className="flex items-center gap-1 rounded-full bg-slate-100 px-3 py-1 font-medium text-slate-600">
          <CalendarDays className="h-3.5 w-3.5" />
          {crop.growth_duration_days} days
        </span>

        {crop.expected_yield_per_acre && (
          <span className="flex items-center gap-1 rounded-full bg-slate-100 px-3 py-1 font-medium text-slate-600">
            <TrendingUp className="h-3.5 w-3.5" />
            {crop.expected_yield_per_acre}
          </span>
        )}
      </div>

      {/* Reasoning */}
      <div className="space-y-1.5 border-t border-slate-100 pt-4 text-sm text-slate-600">
        <p>🌱 {reasoning.soil}</p>
        <p>🗓️ {reasoning.season}</p>
        <p>📍 {reasoning.location}</p>
      </div>
    </div>
  );
}