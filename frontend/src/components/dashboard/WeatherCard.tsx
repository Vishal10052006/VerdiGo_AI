/**
 * ============================================================================
 * Weather Card Component
 * ============================================================================
 */

import {
  CloudSun,
  Droplets,
  Wind,
  CloudRain,
} from "lucide-react";

interface WeatherCardProps {
  temperature: number;
  condition: string;
  humidity: number;
  windSpeed: number;
  rainfall: number;
  provider: string;
}

export default function WeatherCard({
  temperature,
  condition,
  humidity,
  windSpeed,
  rainfall,
  provider,
}: WeatherCardProps) {
  return (
    <section
      className="
        rounded-2xl
        border
        border-slate-200
        bg-white
        p-6
        shadow-sm
      "
    >
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <div className="rounded-xl bg-amber-100 p-3">
            <CloudSun className="h-7 w-7 text-amber-500" />
          </div>

          <div>
            <h2 className="text-xl font-bold">
              Current Weather
            </h2>

            <p className="text-sm text-slate-500">
              Live weather conditions
            </p>
          </div>

        </div>

        <span
          className="
            rounded-full
            bg-green-100
            px-3
            py-1
            text-[11px]
            font-semibold
            text-green-700
          "
        >
          {provider.toUpperCase()}
        </span>

      </div>

      {/* Temperature */}

      <div className="mb-8">

        <h1 className="text-6xl font-bold text-slate-900">
          {Math.round(temperature)}°
        </h1>

        <p className="mt-2 text-lg text-slate-600">
          {condition}
        </p>

      </div>

      {/* Weather Stats */}

      <div className="grid grid-cols-3 gap-6">

        <div className="rounded-xl bg-slate-50 p-4">

          <Droplets className="mb-2 h-6 w-6 text-blue-500" />

          <p className="text-xs text-slate-500">
            Humidity
          </p>

          <h3 className="text-xl font-bold">
            {humidity}%
          </h3>

        </div>

        <div className="rounded-xl bg-slate-50 p-4">

          <Wind className="mb-2 h-6 w-6 text-sky-500" />

          <p className="text-xs text-slate-500">
            Wind
          </p>

          <h3 className="text-xl font-bold">
            {windSpeed} km/h
          </h3>

        </div>

        <div className="rounded-xl bg-slate-50 p-4">

          <CloudRain className="mb-2 h-6 w-6 text-indigo-500" />

          <p className="text-xs text-slate-500">
            Rainfall
          </p>

          <h3 className="text-xl font-bold">
            {rainfall} mm
          </h3>

        </div>

      </div>

    </section>
  );
}