"use client";

import { Eye, Target } from "lucide-react";

export default function Vision() {
  return (
    <section
      id="about"
      className="bg-white py-24"
    >
      <div className="mx-auto w-full max-w-7xl px-6 py-8">

        {/* Heading */}

        <div className="mx-auto mb-16 max-w-3xl text-center">

          <span className="rounded-full bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-700">
            🌍 About VerdiGO
          </span>

          <h2 className="mt-6 text-5xl font-bold">
            Building the Future of Agriculture
          </h2>

          <p className="mt-6 text-lg text-muted-foreground">
            We believe Artificial Intelligence should empower every farmer with
            better decisions, higher productivity, and sustainable farming.
          </p>

        </div>

        {/* Cards */}

        <div className="grid gap-8 lg:grid-cols-2">

          {/* Vision */}

          <div className="rounded-3xl border bg-gradient-to-br from-emerald-50 to-white p-10 shadow-sm">

            <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-100">
              <Eye className="h-8 w-8 text-emerald-600" />
            </div>

            <h3 className="mb-4 text-3xl font-bold">
              Our Vision
            </h3>

            <p className="leading-8 text-muted-foreground">
              To become the world's most trusted AI-powered agriculture platform,
              enabling every farmer to make smarter decisions using data,
              intelligence, and technology.
            </p>

          </div>

          {/* Mission */}

          <div className="rounded-3xl border bg-gradient-to-br from-green-50 to-white p-10 shadow-sm">

            <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-green-100">
              <Target className="h-8 w-8 text-green-600" />
            </div>

            <h3 className="mb-4 text-3xl font-bold">
              Our Mission
            </h3>

            <p className="leading-8 text-muted-foreground">
              Empower farmers through AI-driven crop recommendations, weather
              intelligence, farm management, and predictive analytics to improve
              yield, reduce costs, and promote sustainable agriculture.
            </p>

          </div>

        </div>

      </div>
    </section>
  );
}