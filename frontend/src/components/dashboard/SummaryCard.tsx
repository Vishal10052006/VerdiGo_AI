/**
 * ============================================================================
 * Summary Card Component
 * ============================================================================
 */

import { ReactNode } from "react";
import CountUp from "react-countup";

interface SummaryCardProps {
  title: string;
  value: string | number;
  icon: ReactNode;
  animate?: boolean;
  suffix?: string;
}

export default function SummaryCard({
  title,
  value,
  icon,
  animate = false,
  suffix = "",
}: SummaryCardProps) {
  return (
    <div
      className="
        group
        rounded-2xl
        border
        border-slate-200
        bg-white
        p-6
        shadow-sm
        transition-all
        duration-300
        hover:-translate-y-1
        hover:shadow-xl
      "
    >
      <div className="flex items-start justify-between">

        <div>

          <p className="text-sm font-medium text-slate-500">
            {title}
          </p>

            <h3 className="mt-2 text-4xl font-bold text-slate-900">
            {animate && typeof value === "number" ? (
                <CountUp
                end={value}
                duration={1.5}
                separator=","
                suffix={suffix}
                />
            ) : (
                `${value}${suffix}`
            )}
            </h3>

        </div>

        <div
          className="
            flex
            h-14
            w-14
            items-center
            justify-center
            rounded-2xl
            bg-green-50
            text-green-600
            transition-all
            duration-300
            group-hover:scale-110
          "
        >
          {icon}
        </div>

      </div>
    </div>
  );
}