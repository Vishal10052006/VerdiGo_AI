"use client";

import {
  Brain,
  CloudSun,
  Tractor,
  BarChart3,
  ArrowRight,
} from "lucide-react";

const features = [
  {
    title: "AI Crop Recommendation",
    description:
      "Get intelligent crop suggestions based on soil, weather, and seasonal conditions.",
    icon: Brain,
    color: "text-emerald-600",
    bg: "bg-emerald-100",
  },
  {
    title: "Weather Intelligence",
    description:
      "Receive real-time weather forecasts and alerts to plan farming activities efficiently.",
    icon: CloudSun,
    color: "text-blue-600",
    bg: "bg-blue-100",
  },
  {
    title: "Farm Management",
    description:
      "Manage farms, crops, activities, and resources from one centralized dashboard.",
    icon: Tractor,
    color: "text-orange-600",
    bg: "bg-orange-100",
  },
  {
    title: "Smart Analytics",
    description:
      "Visualize productivity, monitor farm performance, and make data-driven decisions.",
    icon: BarChart3,
    color: "text-purple-600",
    bg: "bg-purple-100",
  },
];

export default function Features() {
  return (
   <section
        id="features"
        className="bg-white py-20"
    >

      <div className="mx-auto max-w-7xl px-6">

        {/* Section Header */}

        <div className="mx-auto mb-16 max-w-3xl text-center">

          <span className="rounded-full bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-700">
            ✨ Platform Features
          </span>

          <h2 className="mt-6 text-5xl font-bold">
            Everything Farmers Need
          </h2>

          <p className="mt-6 text-lg text-muted-foreground">
            VerdiGO combines Artificial Intelligence, Weather Intelligence,
            Farm Management and Smart Analytics into one powerful platform.
          </p>

        </div>

        {/* Cards */}

        <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-4">

          {features.map((feature) => {

            const Icon = feature.icon;

            return (

              <div
                key={feature.title}
                className="group rounded-3xl border bg-white p-8 shadow-sm transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl"
              >

                <div
                  className={`mb-6 flex h-16 w-16 items-center justify-center rounded-2xl ${feature.bg}`}
                >
                  <Icon className={`h-8 w-8 ${feature.color}`} />
                </div>

                <h3 className="mb-4 text-2xl font-semibold">
                  {feature.title}
                </h3>

                <p className="mb-8 leading-7 text-muted-foreground">
                  {feature.description}
                </p>

                <button className="flex items-center gap-2 font-medium text-emerald-600 transition-all group-hover:gap-4">
                  Learn More
                  <ArrowRight className="h-4 w-4" />
                </button>

              </div>

            );

          })}

        </div>

      </div>

    </section>
  );
}