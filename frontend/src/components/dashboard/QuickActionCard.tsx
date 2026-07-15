/**
 * ============================================================================
 * Quick Action Card
 * ============================================================================
 *
 * Reusable action card used on Dashboard.
 *
 * Responsibilities:
 * - Display dashboard action
 * - Hover animation
 * - Navigation arrow
 *
 * Module:
 * Phase 1 → Module 6 → Dashboard
 *
 * Author: VerdiGO Frontend Team
 * ============================================================================
 */

import { ArrowRight } from "lucide-react";
import { ReactNode } from "react";

interface QuickActionCardProps {
  title: string;
  description: string;
  icon: ReactNode;
  onClick?: () => void;
}

export default function QuickActionCard({
  title,
  description,
  icon,
  onClick,
}: QuickActionCardProps) {
  return (
    <button
      onClick={onClick}
      className="
        group
        w-full
        rounded-3xl
        border
        border-slate-200
        bg-white
        p-6
        text-left
        shadow-sm
        transition-all
        duration-300
        hover:-translate-y-1
        hover:border-green-300
        hover:shadow-xl
      "
    >
      <div className="flex items-center justify-between">

        {/* Left */}

        <div className="flex items-center gap-4">

          <div
            className="
              flex
              h-16
              w-16
              items-center
              justify-center
              rounded-2xl
              bg-green-100
              text-green-600
            "
          >
            {icon}
          </div>

          <div>

            <h3 className="text-lg font-semibold text-slate-900">
              {title}
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              {description}
            </p>

          </div>

        </div>

        {/* Arrow */}

        <ArrowRight
          className="
            h-6
            w-6
            text-slate-400
            transition-transform
            duration-300
            group-hover:translate-x-2
            group-hover:text-green-600
          "
        />

      </div>
    </button>
  );
}