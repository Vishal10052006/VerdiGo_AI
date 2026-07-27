// frontend/src/app/weather/page.tsx
"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import Sidebar from "@/components/common/Sidebar";
import { PageHeader } from "@/components/common/PageHeader";
import { LoadingSkeleton } from "@/components/common/LoadingSkeleton";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import WeatherCard from "@/components/dashboard/WeatherCard";
import { getFarm } from "@/services/farm.service";
import { getCurrentWeather, getWeatherAdvisories } from "@/services/weather.service";
import type { CurrentWeather, WeatherAdvisory } from "@/types/weather";
import { CloudSun, AlertTriangle } from "lucide-react";

export default function WeatherPage() {
  const [farmId, setFarmId] = useState<string | null>(null);
  const [weather, setWeather] = useState<CurrentWeather | null>(null);
  const [advisory, setAdvisory] = useState<WeatherAdvisory | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      setError(null);

      try {
        const farm = await getFarm();
        if (cancelled) return;
        setFarmId(farm.id);

        const [weatherData, advisoryData] = await Promise.all([
          getCurrentWeather(farm.id),
          getWeatherAdvisories(farm.id),
        ]);

        if (!cancelled) {
          setWeather(weatherData);
          setAdvisory(advisoryData);
        }
      } catch (err) {
        console.error("Weather fetch error:", err);
        if (!cancelled) {
          setError("Unable to load weather data. Please try again.");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen">
        <Sidebar />

        <main className="flex-1 bg-slate-50">
          <PageHeader
            title="Weather"
            description="Live conditions and farming advisories for your farm"
            icon={<CloudSun className="h-6 w-6" />}
          />

          <div className="mx-auto max-w-4xl space-y-6 px-4 py-6 sm:px-6 lg:px-8">
            {loading ? (
              <LoadingSkeleton variant="card" />
            ) : !farmId ? (
              <EmptyState
                title="No farm registered yet"
                description="Register a farm to see live weather and advisories."
                icon={<CloudSun className="h-10 w-10" />}
              />
            ) : error ? (
              <ErrorState
                title="Unable to load weather"
                description={error}
                actionLabel="Retry"
                onAction={() => window.location.reload()}
              />
            ) : (
              <>
                {weather && (
                  <WeatherCard
                    temperature={weather.temperature}
                    humidity={weather.humidity}
                    windSpeed={weather.wind_speed}
                    rainfall={weather.rainfall}
                    condition={weather.condition}
                    provider={weather.provider}
                  />
                )}

                {advisory && advisory.advisories.length > 0 && (
                  <div className="rounded-3xl border bg-white p-6 shadow-sm">
                    <h2 className="mb-4 text-xl font-bold text-slate-900">
                      Farming Advisories
                    </h2>
                    <div className="space-y-3">
                      {advisory.advisories.map((item, i) => (
                        <div
                          key={i}
                          className="flex items-start gap-3 rounded-xl border-l-4 border-l-amber-400 bg-amber-50 p-4"
                        >
                          <AlertTriangle className="mt-0.5 h-5 w-5 flex-shrink-0 text-amber-600" />
                          <div>
                            <h3 className="font-semibold text-slate-900">{item.title}</h3>
                            <p className="mt-1 text-sm text-slate-600">{item.message}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}