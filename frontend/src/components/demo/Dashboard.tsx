"use client";

import {
  Plus,
  Bot,
  Users,
  Sprout,
  Brain,
  CloudRain,
  CloudSun,
} from "lucide-react";

export default function Dashboard() {
  return (
    <section className="bg-slate-50 py-16">
      <div className="mx-auto max-w-7xl px-6">

        {/* Header */}
        <div className="mb-10">

          <span className="rounded-full bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-700">
            🌱 Demo Dashboard
          </span>

          <h1 className="mt-6 text-5xl font-bold">
            Welcome to VerdiGO AI
          </h1>

          <p className="mt-4 max-w-3xl text-lg text-slate-600">
            Experience how Artificial Intelligence helps farmers monitor crops,
            weather, farm health and productivity — all without login.
          </p>

        </div>

        {/* Welcome Banner */}
        <div className="rounded-3xl border bg-white p-8 shadow-sm">

          <div className="flex flex-col gap-10 lg:flex-row lg:items-center lg:justify-between">

            {/* Left */}
            <div>

              <div className="inline-flex rounded-full bg-orange-100 px-4 py-2 text-sm font-semibold text-orange-700">
                🚀 Demo Mode
              </div>

              <h2 className="mt-5 text-3xl font-bold">
                Good Morning 👋
              </h2>

              <p className="mt-3 max-w-xl text-slate-600">
                Your farms are performing well today. AI has analyzed current
                weather conditions and generated smart recommendations for
                maximum productivity.
              </p>

            </div>

            {/* Right */}
            <div className="flex flex-wrap gap-4">

              <button className="flex items-center gap-2 rounded-xl bg-emerald-600 px-5 py-3 font-medium text-white transition hover:bg-emerald-700">
                <Plus className="h-5 w-5" />
                Add Farm
              </button>

              <button className="flex items-center gap-2 rounded-xl border px-5 py-3 transition hover:bg-slate-50">
                <Bot className="h-5 w-5 text-emerald-600" />
                AI Assistant
              </button>

              <button className="flex items-center gap-2 rounded-xl border px-5 py-3 transition hover:bg-slate-50">
                <CloudSun className="h-5 w-5 text-blue-600" />
                Weather
              </button>

            </div>

          </div>

          {/* Statistics */}
          <div className="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-4">

            <div className="rounded-2xl border p-6">
              <Users className="mb-4 h-8 w-8 text-emerald-600" />
              <p className="text-3xl font-bold">1,250</p>
              <p className="text-slate-500">Farmers</p>
            </div>

            <div className="rounded-2xl border p-6">
              <Sprout className="mb-4 h-8 w-8 text-green-600" />
              <p className="text-3xl font-bold">4,870</p>
              <p className="text-slate-500">Farms</p>
            </div>

            <div className="rounded-2xl border p-6">
              <Brain className="mb-4 h-8 w-8 text-purple-600" />
              <p className="text-3xl font-bold">8</p>
              <p className="text-slate-500">AI Modules</p>
            </div>

            <div className="rounded-2xl border p-6">
              <CloudRain className="mb-4 h-8 w-8 text-blue-600" />
              <p className="text-3xl font-bold">32</p>
              <p className="text-slate-500">Weather Updates</p>
            </div>

          </div>

        {/* Weather Section */}
        <div className="mt-10 grid gap-6 lg:grid-cols-3">

        {/* Current Weather */}
        <div className="rounded-3xl border bg-white p-6 shadow-sm">

            <div className="mb-6 flex items-center justify-between">
            <h3 className="text-xl font-bold">Current Weather</h3>
            <CloudSun className="h-8 w-8 text-yellow-500" />
            </div>

            <p className="text-5xl font-bold">28°C</p>

            <p className="mt-2 text-slate-600">
            Partly Cloudy
            </p>

            <div className="mt-6 space-y-3 text-sm">

            <div className="flex justify-between">
                <span>Humidity</span>
                <span className="font-semibold">68%</span>
            </div>

            <div className="flex justify-between">
                <span>Wind</span>
                <span className="font-semibold">12 km/h</span>
            </div>

            <div className="flex justify-between">
                <span>Rain Chance</span>
                <span className="font-semibold">25%</span>
            </div>

            </div>

        </div>

        {/* Forecast */}
        <div className="rounded-3xl border bg-white p-6 shadow-sm lg:col-span-2">

            <h3 className="mb-6 text-xl font-bold">
            5 Day Forecast
            </h3>

            <div className="space-y-4">

            {[
                ["Today", "☀️", "28°C"],
                ["Tomorrow", "🌤", "30°C"],
                ["Wednesday", "🌦", "27°C"],
                ["Thursday", "🌧", "25°C"],
                ["Friday", "☀️", "29°C"],
            ].map(([day, icon, temp]) => (

                <div
                key={day}
                className="flex items-center justify-between rounded-xl border p-4"
                >
                <div className="flex items-center gap-4">
                    <span className="text-2xl">{icon}</span>

                    <span className="font-medium">
                    {day}
                    </span>
                </div>

                <span className="font-bold">
                    {temp}
                </span>

                </div>

            ))}

            </div>

        </div>

        </div>
        </div>

        {/* ================= Farm Overview ================= */}

        <div className="mt-10">

        <div className="mb-6">
            <h2 className="text-3xl font-bold">
            Farm Overview
            </h2>

            <p className="mt-2 text-slate-600">
            Monitor your registered farms and their current health status.
            </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">

            {/* Farm Card */}

            <div className="rounded-3xl border bg-white p-8 shadow-sm">

            <div className="mb-6 flex items-center justify-between">

                <div>

                <h3 className="text-2xl font-bold">
                    Demo Wheat Farm
                </h3>

                <p className="text-slate-500">
                    Madhya Pradesh
                </p>

                </div>

                <span className="rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
                Healthy
                </span>

            </div>

            <div className="grid gap-4 sm:grid-cols-2">

                <div className="rounded-2xl bg-slate-50 p-5">
                <p className="text-sm text-slate-500">
                    Soil Type
                </p>

                <p className="mt-2 text-xl font-bold">
                    Black Soil
                </p>
                </div>

                <div className="rounded-2xl bg-slate-50 p-5">
                <p className="text-sm text-slate-500">
                    Area
                </p>

                <p className="mt-2 text-xl font-bold">
                    12 Acres
                </p>
                </div>

                <div className="rounded-2xl bg-slate-50 p-5">
                <p className="text-sm text-slate-500">
                    Crop
                </p>

                <p className="mt-2 text-xl font-bold">
                    Wheat
                </p>
                </div>

                <div className="rounded-2xl bg-slate-50 p-5">
                <p className="text-sm text-slate-500">
                    Last Updated
                </p>

                <p className="mt-2 text-xl font-bold">
                    Today
                </p>
                </div>

            </div>

            </div>

            {/* Farm Status */}

            <div className="rounded-3xl border bg-white p-8 shadow-sm">

            <h3 className="mb-6 text-2xl font-bold">
                Farm Status
            </h3>

            <div className="space-y-5">

                <div>

                <div className="mb-2 flex justify-between">
                    <span>Crop Health</span>
                    <span className="font-semibold text-green-600">
                    92%
                    </span>
                </div>

                <div className="h-3 rounded-full bg-slate-200">
                    <div className="h-3 w-[92%] rounded-full bg-green-500"></div>
                </div>

                </div>

                <div>

                <div className="mb-2 flex justify-between">
                    <span>Soil Moisture</span>
                    <span className="font-semibold text-blue-600">
                    68%
                    </span>
                </div>

                <div className="h-3 rounded-full bg-slate-200">
                    <div className="h-3 w-[68%] rounded-full bg-blue-500"></div>
                </div>

                </div>

                <div>

                <div className="mb-2 flex justify-between">
                    <span>Growth Stage</span>
                    <span className="font-semibold text-emerald-600">
                    Vegetative
                    </span>
                </div>

                <div className="h-3 rounded-full bg-slate-200">
                    <div className="h-3 w-[78%] rounded-full bg-emerald-500"></div>
                </div>

                </div>

            </div>

            </div>

        </div>
        </div>


    {/* ================= AI Insights ================= */}

    <div className="mt-10">

    <div className="mb-6">
        <h2 className="text-3xl font-bold">
        AI Insights
        </h2>

        <p className="mt-2 text-slate-600">
        Artificial Intelligence recommendations generated from your farm data.
        </p>
    </div>

    <div className="grid gap-6 lg:grid-cols-3">

        {/* Today's Insight */}

        <div className="rounded-3xl border bg-white p-8 shadow-sm">

        <div className="mb-5 text-5xl">
            🤖
        </div>

        <h3 className="text-2xl font-bold">
            Today's AI Insight
        </h3>

        <p className="mt-4 text-slate-600">
            Soil moisture is expected to decrease tomorrow due to increasing
            temperatures.
        </p>

        </div>

        {/* Recommendation */}

        <div className="rounded-3xl border bg-white p-8 shadow-sm">

        <div className="mb-5 text-5xl">
            🌱
        </div>

        <h3 className="text-2xl font-bold">
            Crop Recommendation
        </h3>

        <p className="mt-4 text-slate-600">
            Irrigate after 24 hours and apply Nitrogen fertilizer within this week
            for higher productivity.
        </p>

        </div>

        {/* Confidence */}

        <div className="rounded-3xl border bg-white p-8 shadow-sm">

        <div className="mb-5 flex items-center justify-between">

            <div>

            <h3 className="text-2xl font-bold">
                AI Confidence
            </h3>

            <p className="text-slate-500">
                Prediction Accuracy
            </p>

            </div>

            <span className="text-4xl">
            🎯
            </span>

        </div>

        <p className="mb-3 text-5xl font-bold text-emerald-600">
            96%
        </p>

        <div className="h-3 rounded-full bg-slate-200">

            <div className="h-3 w-[96%] rounded-full bg-emerald-500"></div>

        </div>

        </div>

    </div>

    {/* ================= Future Roadmap ================= */}

    <div className="mt-16">

    <div className="mb-6">
        <h2 className="text-3xl font-bold">
        Future Roadmap
        </h2>

        <p className="mt-2 text-slate-600">
        Upcoming AI innovations that will make VerdiGO even smarter.
        </p>
    </div>

    <div className="grid gap-6 md:grid-cols-3">

        {/* Disease Detection */}

        <div className="rounded-3xl border bg-white p-8 shadow-sm transition hover:-translate-y-2 hover:shadow-xl">

        <div className="mb-5 text-5xl">
            🦠
        </div>

        <h3 className="text-2xl font-bold">
            Disease Detection
        </h3>

        <p className="mt-4 text-slate-600">
            Detect crop diseases instantly using AI-powered image analysis.
        </p>

        <span className="mt-6 inline-block rounded-full bg-orange-100 px-4 py-2 text-sm font-medium text-orange-700">
            Coming Soon
        </span>

        </div>

        {/* Voice Assistant */}

        <div className="rounded-3xl border bg-white p-8 shadow-sm transition hover:-translate-y-2 hover:shadow-xl">

        <div className="mb-5 text-5xl">
            🎤
        </div>

        <h3 className="text-2xl font-bold">
            Voice Assistant
        </h3>

        <p className="mt-4 text-slate-600">
            Talk to VerdiGO in your local language for farming assistance.
        </p>

        <span className="mt-6 inline-block rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
            Coming Soon
        </span>

        </div>

        {/* Market Intelligence */}

        <div className="rounded-3xl border bg-white p-8 shadow-sm transition hover:-translate-y-2 hover:shadow-xl">

        <div className="mb-5 text-5xl">
            📈
        </div>

        <h3 className="text-2xl font-bold">
            Market Intelligence
        </h3>

        <p className="mt-4 text-slate-600">
            Predict crop prices and discover the best selling opportunities.
        </p>

        <span className="mt-6 inline-block rounded-full bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-700">
            Phase 2
        </span>

        </div>

    </div>

    </div>

    </div>

    </div>
    </section>
  );
}