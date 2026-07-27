"use client";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import AuthenticatedLayout from "@/layouts/AuthenticatedLayout";
import Greeting from "@/components/dashboard/Greeting";
import SummaryCards from "@/components/dashboard/SummaryCards";
import WeatherCard from "@/components/dashboard/WeatherCard";
import QuickActions from "@/components/dashboard/QuickActions";
import RecentActivity from "@/components/dashboard/RecentActivity";
import FarmSummaryCard from "@/components/dashboard/FarmSummaryCard";
import DashboardSkeleton from "@/components/dashboard/DashboardSkeleton";
import { ErrorState } from "@/components/common/ErrorState";
import { motion } from "framer-motion";

import { useDashboard } from "@/hooks/useDashboard";
import { CloudSun } from "lucide-react";

export default function DashboardPage() {
  const { dashboard, loading, error, refetch } = useDashboard();

  if (loading) {
    return (
      <ProtectedRoute>
        <AuthenticatedLayout>
          <DashboardSkeleton />
        </AuthenticatedLayout>
      </ProtectedRoute>
    );
  }

  if (error || !dashboard) {
    return (
      <ProtectedRoute>
        <AuthenticatedLayout>
          <div className="flex min-h-full items-center justify-center">
            <ErrorState
              title="Unable to load dashboard"
              description={error ?? "Something went wrong. Please try again."}
              actionLabel="Retry"
              onAction={refetch}
            />
          </div>
        </AuthenticatedLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AuthenticatedLayout>
        <div className="mx-auto max-w-[1600px] px-4 py-6 sm:px-6 lg:px-8">
          <section className="mb-10">
            <h1 className="text-4xl font-bold tracking-tight text-slate-900">
              Dashboard
            </h1>
            <p className="mt-2 text-slate-500">
              Welcome back! Here&apos;s what&apos;s happening across your farm today.
            </p>
          </section>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35 }}
          >
            <Greeting fullName={dashboard.farmer.full_name} />
          </motion.div>

          <SummaryCards
            totalFarms={dashboard.statistics.total_farms}
            profileCompleted={dashboard.statistics.profile_completed}
            completionPercentage={dashboard.statistics.completion_percentage}
            registeredDays={dashboard.statistics.registered_days}
          />

          <section className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
            {dashboard.weather ? (
              <WeatherCard
                temperature={dashboard.weather.temperature}
                humidity={dashboard.weather.humidity}
                windSpeed={dashboard.weather.wind_speed}
                rainfall={dashboard.weather.rainfall}
                condition={dashboard.weather.condition}
                provider={dashboard.weather.provider}
              />
            ) : (
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <p className="text-sm text-slate-500">
                  Weather data isn't available yet for your farm. This usually resolves once your
                  farm's location is fully set up.
                </p>
              </div>
            )}

            {dashboard.primary_farm ? (
              <FarmSummaryCard
                farmName={dashboard.primary_farm.farm_name}
                village={dashboard.primary_farm.village}
                district={dashboard.primary_farm.district}
                state={dashboard.primary_farm.state}
                soilType={dashboard.farms[0]?.soil_type ?? "Unknown"}
                landArea={dashboard.farms[0]?.land_area ?? "0"}
                landUnit={dashboard.farms[0]?.land_unit ?? ""}
                totalFarms={dashboard.statistics.total_farms}
              />
            ) : (
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <p className="text-sm text-slate-500">No farm registered yet.</p>
              </div>
            )}
          </section>

          <QuickActions />
          <RecentActivity />
        </div>
      </AuthenticatedLayout>
    </ProtectedRoute>
  );
}