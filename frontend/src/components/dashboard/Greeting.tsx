/**
 * ============================================================================
 * Greeting Component
 * ============================================================================
 *
 * Premium greeting section for Dashboard.
 *
 * Responsibilities:
 * - Welcome the authenticated farmer
 * - Display dynamic greeting
 * - Display profile avatar
 * - Responsive hero banner
 *
 * Module:
 * Phase 1 → Module 6 → Dashboard
 *
 * Author: VerdiGO Frontend Team
 * ============================================================================
 */

"use client";

import { CloudSun } from "lucide-react";

interface GreetingProps {
  fullName: string;
}

export default function Greeting({
  fullName,
}: GreetingProps) {

  /**
   * --------------------------------------------------------------------------
   * Dynamic Greeting
   * --------------------------------------------------------------------------
   */

  const hour = new Date().getHours();

  let greeting = "Good Evening";

  if (hour < 12) {
    greeting = "Good Morning";
  } else if (hour < 17) {
    greeting = "Good Afternoon";
  }

  /**
   * --------------------------------------------------------------------------
   * Avatar Letter
   * --------------------------------------------------------------------------
   */

  const avatar = fullName.charAt(0).toUpperCase();

  return (
    <section
      className="
        rounded-3xl
        bg-gradient-to-r
        from-green-600
        via-emerald-600
        to-green-700
        p-8
        text-white
        shadow-lg
      "
    >
      <div
        className="
          flex
          flex-col
          gap-8
          lg:flex-row
          lg:items-center
          lg:justify-between
        "
      >
        {/* ================================================================ */}
        {/* Left Content */}
        {/* ================================================================ */}

        <div>

          <div className="flex items-center gap-2 text-green-100">

            <CloudSun className="h-5 w-5" />

            <span className="text-sm font-medium">
              {greeting}
            </span>

          </div>

          <h1 className="mt-4 text-4xl font-bold tracking-tight">

            Welcome back,

          </h1>

          <h2 className="mt-2 text-5xl font-extrabold">

            {fullName}

          </h2>

          <p className="mt-5 max-w-xl text-green-100">

            Here's a quick overview of your farm,
            weather conditions, and recent activities.

          </p>

        </div>

        {/* ================================================================ */}
        {/* Right Avatar */}
        {/* ================================================================ */}

        <div
          className="
            flex
            h-24
            w-24
            items-center
            justify-center
            rounded-full
            border-4
            border-white/40
            bg-white/20
            text-5xl
            font-bold
            backdrop-blur-md
          "
        >
          {avatar}
        </div>

      </div>
    </section>
  );
}