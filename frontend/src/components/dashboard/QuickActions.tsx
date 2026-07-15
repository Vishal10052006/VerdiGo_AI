/**
 * ============================================================================
 * Quick Actions
 * ============================================================================
 *
 * Displays dashboard quick action cards.
 *
 * Responsibilities:
 * - Add Farm
 * - View Farms
 *
 * Module:
 * Phase 1 → Module 6 → Dashboard
 *
 * Author: VerdiGO Frontend Team
 * ============================================================================
 */

import {
  Plus,
  Tractor,
} from "lucide-react";

import CountUp from "react-countup";

import QuickActionCard from "./QuickActionCard";

export default function QuickActions() {
  return (
    <div className="mt-10">
        <h2 className="mb-4 flex items-center gap-2 text-xl font-bold text-slate-900">
          ⚡ Quick Actions
        </h2>

        <div className="grid gap-6 md:grid-cols-2">

            <QuickActionCard
            title="Add Farm"
            description="Register a new farm"
            icon={<Plus className="h-8 w-8" />}
            onClick={() => console.log("Navigate to Add Farm")}
            />

            <QuickActionCard
            title="View Farms"
            description="Manage all your farms"
            icon={<Tractor className="h-8 w-8 text-blue-600" />}
            onClick={() => console.log("Navigate to Farms")}
            />

        </div>
    </div>
  );
}