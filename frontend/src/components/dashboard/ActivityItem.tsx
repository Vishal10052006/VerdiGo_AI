/**
 * ============================================================================
 * Activity Item
 * ============================================================================
 *
 * Reusable timeline activity item.
 *
 * Responsibilities:
 * - Display icon
 * - Display activity title
 * - Display description
 * - Display timestamp
 *
 * Module:
 * Phase 1 → Module 6 → Dashboard
 *
 * Author: VerdiGO Frontend Team
 * ============================================================================
 */

import { ReactNode } from "react";

interface ActivityItemProps {
  icon: ReactNode;
  title: string;
  description: string;
  time: string;
}

export default function ActivityItem({
  icon,
  title,
  description,
  time,
}: ActivityItemProps) {
  return (
    <div
      className="
        flex
        items-start
        gap-4
        rounded-2xl
        border
        border-slate-200
        bg-white
        p-5
        transition-all
        duration-300
        hover:-translate-y-1
        hover:shadow-md
      "
    >
      <div className="rounded-xl bg-green-100 p-3">
        {icon}
      </div>

      <div className="flex-1">
        <h3 className="font-semibold text-slate-900">
          {title}
        </h3>

        <p className="mt-1 text-sm text-slate-500">
          {description}
        </p>
      </div>

      <span className="text-xs text-slate-400">
        {time}
      </span>
    </div>
  );
}