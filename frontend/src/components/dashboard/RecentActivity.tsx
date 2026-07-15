/**
 * ============================================================================
 * Recent Activity
 * ============================================================================
 *
 * Dashboard activity timeline.
 *
 * Module:
 * Phase 1 → Module 6 → Dashboard
 *
 * Author: VerdiGO Frontend Team
 * ============================================================================
 */

import {
  Clock3,
  Tractor,
  UserCircle,
} from "lucide-react";

import ActivityItem from "./ActivityItem";

interface RecentActivityProps {
  hasActivity?: boolean;
}

export default function RecentActivity({
  hasActivity = false,
}: RecentActivityProps) {
  return (
    <section
      className="
        mt-10
        rounded-3xl
        border
        border-slate-200
        bg-white
        p-6
        shadow-sm
      "
    >
      <div className="mb-6 flex items-center gap-3">
        <Clock3 className="h-6 w-6 text-indigo-600" />

        <h2 className="mb-4 flex items-center gap-2 text-xl font-bold text-slate-900">
          🕒 Recent Activity
        </h2>
      </div>

      {!hasActivity ? (
        <div
          className="
            flex
            min-h-[220px]
            flex-col
            items-center
            justify-center
            rounded-2xl
            border-2
            border-dashed
            border-slate-200
            bg-slate-50
            text-center
          "
        >
          <Clock3 className="mb-4 h-12 w-12 text-slate-300" />

          <h3 className="text-lg font-semibold">
            🌱 Your farming journey starts here.

            Weather updates,
            crop recommendations,
            AI insights and farm activities

            will appear automatically.
          </h3>

          <p className="mt-2 max-w-md text-sm text-slate-500">
            Your farming activities, weather updates,
            and future AI recommendations will appear
            here.
          </p>
        </div>
      ) : (
        <div className="space-y-4">

          <ActivityItem
            icon={
              <UserCircle className="h-6 w-6 text-blue-600" />
            }
            title="Profile Completed"
            description="Your farmer profile has been updated."
            time="Today"
          />

          <ActivityItem
            icon={
              <Tractor className="h-6 w-6 text-green-600" />
            }
            title="Farm Registered"
            description="MY FARMER has been added."
            time="Yesterday"
          />

        </div>
      )}
    </section>
  );
}