/**
 * ============================================================================
 * Summary Cards Component
 * ============================================================================
 *
 * Displays all dashboard summary cards.
 *
 * Responsibilities:
 * - Render dashboard statistics
 * - Responsive grid layout
 * - Reuse SummaryCard component
 *
 * Module:
 * Phase 1 → Module 6 → Dashboard
 *
 * Author: VerdiGO Frontend Team
 * ============================================================================
 */

import {
  CalendarDays,
  CheckCircle2,
  Sprout,
  UserCircle,
} from "lucide-react";

import { motion } from "framer-motion";

import SummaryCard from "./SummaryCard";

/**
 * ============================================================================
 * Component Props
 * ============================================================================
 */

interface SummaryCardsProps {
  totalFarms: number;
  profileCompleted: boolean;
  completionPercentage: number;
  registeredDays: number;
}

/**
 * ============================================================================
 * Summary Cards
 * ============================================================================
 */

export default function SummaryCards({
  totalFarms,
  profileCompleted,
  completionPercentage,
  registeredDays,
}: SummaryCardsProps) {
  return (
    <section
      className="
        mt-8
        grid
        gap-6
        grid-cols-1
        sm:grid-cols-2
        xl:grid-cols-4
      "
    >
        <SummaryCard
        title="Total Farms"
        value={totalFarms}
        animate
        icon={<Sprout className="h-7 w-7 text-green-600" />}
        />

      <SummaryCard
        title="Profile Status"
        value={profileCompleted ? "Completed" : "Incomplete"}
        icon={<UserCircle className="h-7 w-7 text-blue-600" />}
      />

      <SummaryCard
        title="Completion"
        value={completionPercentage}
        animate
        suffix="%"
        icon={<CheckCircle2 className="h-7 w-7 text-emerald-600" />}
        />

      <SummaryCard
        title="Registered"
        value={registeredDays}
        animate
        suffix=" Days"
        icon={<CalendarDays className="h-7 w-7 text-orange-500" />}
        />
    </section>
  );
}