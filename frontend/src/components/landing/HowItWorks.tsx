"use client";

import {
  MapPinned,
  Brain,
  Sparkles,
  TrendingUp,
} from "lucide-react";

const steps = [
  {
    number: "01",
    title: "Register Farm",
    description:
      "Add your farm location, crop information and basic details to get started.",
    icon: MapPinned,
    color: "text-emerald-600",
    bg: "bg-emerald-100",
  },
  {
    number: "02",
    title: "AI Analysis",
    description:
      "VerdiGO analyzes soil, weather and crop data using Artificial Intelligence.",
    icon: Brain,
    color: "text-blue-600",
    bg: "bg-blue-100",
  },
  {
    number: "03",
    title: "Smart Recommendations",
    description:
      "Receive personalized irrigation, fertilizer and crop recommendations.",
    icon: Sparkles,
    color: "text-orange-600",
    bg: "bg-orange-100",
  },
  {
    number: "04",
    title: "Increase Yield",
    description:
      "Improve productivity, reduce farming costs and maximize profits.",
    icon: TrendingUp,
    color: "text-purple-600",
    bg: "bg-purple-100",
  },
];

export default function HowItWorks() {
  return (
    <section
        id="how-it-works"
        className="bg-emerald-50 py-24"
    >
      <div className="mx-auto w-full max-w-7xl px-6 py-8">
        {/* Header */}
        <div className="mx-auto mb-20 max-w-3xl text-center">
          <span className="rounded-full bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-700">
            🚀 How It Works
          </span>

          <h2 className="mt-6 text-5xl font-bold">
            Start Smart Farming in 4 Steps
          </h2>

          <p className="mt-6 text-lg text-muted-foreground">
            VerdiGO simplifies modern farming through Artificial Intelligence,
            weather intelligence and data-driven recommendations.
          </p>
        </div>

        {/* Steps */}
        <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-4">
          {steps.map((step) => {
            const Icon = step.icon;

            return (
              <div
                key={step.number}
                className="group relative rounded-3xl bg-white p-8 shadow-sm transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl"
              >
                <span className="absolute right-6 top-6 text-5xl font-bold text-gray-100">
                  {step.number}
                </span>

                <div
                  className={`mb-6 flex h-16 w-16 items-center justify-center rounded-2xl ${step.bg}`}
                >
                  <Icon className={`h-8 w-8 ${step.color}`} />
                </div>

                <h3 className="mb-4 text-2xl font-semibold">
                  {step.title}
                </h3>

                <p className="leading-7 text-muted-foreground">
                  {step.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}