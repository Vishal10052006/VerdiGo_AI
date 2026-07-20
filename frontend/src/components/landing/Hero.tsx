"use client";

import { Button } from "@/components/ui/button";
import {
  ArrowRight,
  Sparkles,
  CloudSun,
  BarChart3,
} from "lucide-react";

import Link from "next/link";

export default function Hero() {
  return (
    <section
        id="hero"
        className="relative overflow-hidden bg-gradient-to-b from-emerald-50 via-white to-white pt-20"
    >

      {/* Background Blur */}
      <div className="absolute -top-32 -left-32 h-96 w-96 rounded-full bg-emerald-300/20 blur-3xl" />
      <div className="absolute top-40 -right-24 h-80 w-80 rounded-full bg-green-200/20 blur-3xl" />

      <div className="relative mx-auto flex min-h-[100vh] max-w-7xl items-center px-6 py-10">

        <div className="grid items-center gap-16 lg:min-h-[75vh] lg:grid-cols-2">

          {/* LEFT */}

          <div>

            <span className="inline-flex items-center gap-2 rounded-full bg-emerald-100 px-5 py-2 text-sm font-medium text-emerald-700">
              🌱 AI Powered Agriculture Platform
            </span>

            <h1 className="mt-8 text-6xl font-extrabold leading-tight lg:text-7xl">
              Smart Farming
              <br />
              Begins with{" "}
              <span className="bg-gradient-to-r from-emerald-500 to-green-700 bg-clip-text text-transparent">
                AI
              </span>
            </h1>

            <p className="mt-8 max-w-2xl text-lg leading-8 text-muted-foreground">
              VerdiGO empowers farmers with AI-driven crop recommendations,
              real-time weather intelligence, farm management, and smart
              analytics to improve productivity, reduce costs, and increase
              profits.
            </p>

            <div className="mt-10 flex flex-wrap gap-4">

              <Link href="/login">
                <Button
                  size="lg"
                  className="rounded-xl px-8"
                >
                  Start Farming Smarter
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>

              <Button
                size="lg"
                variant="outline"
                className="rounded-xl px-8"
              >
                Book Demo
              </Button>

            </div>

            {/* Trust Pills */}

            <div className="mt-10 flex flex-wrap gap-4">

              <div className="flex items-center gap-2 rounded-full border bg-white px-5 py-3 shadow-sm">
                <Sparkles className="h-4 w-4 text-emerald-600" />
                <span className="text-sm font-medium">
                  AI Powered
                </span>
              </div>

              <div className="flex items-center gap-2 rounded-full border bg-white px-5 py-3 shadow-sm">
                <CloudSun className="h-4 w-4 text-blue-500" />
                <span className="text-sm font-medium">
                  Live Weather
                </span>
              </div>

              <div className="flex items-center gap-2 rounded-full border bg-white px-5 py-3 shadow-sm">
                <BarChart3 className="h-4 w-4 text-orange-500" />
                <span className="text-sm font-medium">
                  Smart Analytics
                </span>
              </div>

            </div>

          </div>

          {/* RIGHT */}

          <div className="relative">

            <div className="absolute inset-0 rounded-3xl bg-emerald-300/20 blur-3xl" />

            <div className="relative rounded-3xl border bg-white p-8 shadow-2xl">

              <div className="mb-8 flex items-center justify-between">

                <div>

                  <p className="text-sm text-muted-foreground">
                    Today's Farm Status
                  </p>

                  <h3 className="text-2xl font-bold">
                    Healthy 🌾
                  </h3>

                </div>

                <div className="rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
                  92%
                </div>

              </div>

              <div className="space-y-4">

                <div className="flex items-center justify-between rounded-xl border p-4">
                  <span>🌦 Weather</span>
                  <span className="font-semibold">28°C</span>
                </div>

                <div className="flex items-center justify-between rounded-xl border p-4">
                  <span>💧 Soil Moisture</span>
                  <span className="font-semibold">68%</span>
                </div>

                <div className="flex items-center justify-between rounded-xl border p-4">
                  <span>🌱 Crop Health</span>
                  <span className="font-semibold text-green-600">
                    Excellent
                  </span>
                </div>

                <div className="flex items-center justify-between rounded-xl border p-4">
                  <span>🤖 AI Recommendation</span>
                  <span className="font-semibold text-emerald-600">
                    Irrigate Tomorrow
                  </span>
                </div>

                <div className="flex items-center justify-between rounded-xl border p-4">
                  <span>📈 Yield Prediction</span>
                  <span className="font-semibold">
                    +18%
                  </span>
                </div>

              </div>

            </div>

          </div>

        </div>

      </div>

    </section>
  );
}