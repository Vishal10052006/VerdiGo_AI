/**
 * ============================================================================
 * Farm Summary Card
 * ============================================================================
 *
 * Premium dashboard card showing the farmer's primary farm.
 *
 * Responsibilities:
 * - Display primary farm
 * - Display location
 * - Display soil
 * - Display area
 * - Display total farms
 *
 * Module:
 * Phase 1 → Module 6 → Dashboard
 *
 * Author: VerdiGO Frontend Team
 * ============================================================================
 */

import {
  Tractor,
  MapPin,
  Sprout,
  Ruler,
  Trees,
  ArrowRight,
} from "lucide-react";

interface FarmSummaryCardProps {
  farmName: string;
  village: string;
  district: string;
  state: string;

  soilType: string;
  landArea: string;
  landUnit: string;

  totalFarms: number;
}

export default function FarmSummaryCard({
  farmName,
  village,
  district,
  state,
  soilType,
  landArea,
  landUnit,
  totalFarms,
}: FarmSummaryCardProps) {
  return (
    <section
      className="
        rounded-3xl
        border
        border-slate-200
        bg-white
        p-6
        shadow-sm
      "
    >
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">

        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-green-100 p-2">
            <Tractor className="h-6 w-6 text-green-600" />
          </div>

          <div>
            <h2 className="text-xl font-bold">
              Farm Summary
            </h2>

            <p className="text-sm text-slate-500">
              Primary farm details
            </p>
          </div>
        </div>

        <span
          className="
            rounded-full
            bg-green-100
            px-3
            py-1
            text-xs
            font-semibold
            text-green-700
          "
        >
          Primary
        </span>

      </div>

      {/* Farm Name */}

      <h3 className="text-2xl font-bold text-slate-900">
        {farmName}
      </h3>

      {/* Location */}

      <div className="mt-3 flex items-center gap-2 text-slate-600">

        <MapPin className="h-5 w-5 text-red-500" />

        {village === "string" ? (
          <span className="text-slate-400">
            Location not available
          </span>
        ) : (
          `${village}, ${district}, ${state}`
        )}

      </div>

      {/* Stats */}

      <div className="mt-8 grid grid-cols-3 gap-4">

        <div className="rounded-2xl bg-slate-50 p-4">

          <Sprout className="mb-2 h-5 w-5 text-green-600" />

          <p className="text-xs text-slate-500">
            Soil
          </p>

          <h4 className="mt-1 font-semibold">
            {soilType}
          </h4>

        </div>

        <div className="rounded-2xl bg-slate-50 p-4">

          <Ruler className="mb-2 h-5 w-5 text-blue-600" />

          <p className="text-xs text-slate-500">
            Area
          </p>

          <h4 className="mt-1 font-semibold">
            {landArea} {landUnit}
          </h4>

        </div>

        <div className="rounded-2xl bg-slate-50 p-4">

          <Trees className="mb-2 h-5 w-5 text-emerald-600" />

          <p className="text-xs text-slate-500">
            Farms
          </p>

          <h4 className="mt-1 font-semibold">
            {totalFarms}
          </h4>

        </div>

      </div>

    </section>
  );
}