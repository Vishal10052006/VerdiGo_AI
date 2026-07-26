/**
 * ============================================================================
 * Quick Actions
 * ============================================================================
 *
 * Displays dashboard quick action cards.
 *
 * Module:
 * Phase 1 → Module 6 → Crop Recommendation
 * ============================================================================
 */

import {
  Plus,
  Tractor,
  Wheat,
  Bug,
} from "lucide-react";

import { useRouter } from "next/navigation";

import QuickActionCard from "./QuickActionCard";

export default function QuickActions() {
  const router = useRouter();

  return (
    <div className="mt-10">
        <h2 className="mb-4 flex items-center gap-2 text-xl font-bold text-slate-900">
          ⚡ Quick Actions
        </h2>

        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">

            <QuickActionCard
              title="Add Farm"
              description="Register a new farm"
              icon={<Plus className="h-8 w-8" />}
              onClick={() => router.push("/farm")}
            />

            <QuickActionCard
              title="View Farm"
              description="Edit your farm details"
              icon={<Tractor className="h-8 w-8 text-blue-600" />}
              onClick={() => router.push("/farm")}
            />

            <QuickActionCard
            title="Crop Recommendation"
            description="AI-powered crop suggestions"
            icon={<Wheat className="h-8 w-8 text-amber-600" />}
            onClick={() => router.push("/crop-recommendation")}
            />

            <QuickActionCard
            title="Disease Detection"
            description="Scan crops for diseases"
            icon={<Bug className="h-8 w-8 text-red-600" />}
            onClick={() => router.push("/disease-detection")}
            />

        </div>
    </div>
  );
}