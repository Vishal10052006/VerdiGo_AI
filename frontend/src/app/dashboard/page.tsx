"use client";

import { useEffect, useState } from "react";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import Greeting from "@/components/dashboard/Greeting";

import { getDashboard } from "@/services/dashboard.service";

import SummaryCards from "@/components/dashboard/SummaryCards";
import WeatherCard from "@/components/dashboard/WeatherCard";
import QuickActions from "@/components/dashboard/QuickActions";
import RecentActivity from "@/components/dashboard/RecentActivity";
import FarmSummaryCard from "@/components/dashboard/FarmSummaryCard";
import DashboardSkeleton from "@/components/dashboard/DashboardSkeleton";
import { motion } from "framer-motion";


/**
 * Dashboard Response Type
 *
 * NOTE:
 * This mirrors the backend response.
 * Later we'll move this into a shared TypeScript interface.
 */
interface DashboardResponse {
  farmer: {
    full_name: string;
  };

  statistics: {
    total_farms: number;
    profile_completed: boolean;
    completion_percentage: number;
    registered_days: number;
  };

  weather: {
    temperature: number;
    humidity: number;
    wind_speed: number;
    rainfall: number;
    condition: string;
    provider: string;
  };

  primary_farm: {
    farm_name: string;
    village: string;
    district: string;
    state: string;
  };

  farms: {
    land_area: string;
    land_unit: string;
    soil_type: string;
  }[];
}

export default function DashboardPage() {
  const [dashboard, setDashboard] =
    useState<DashboardResponse | null>(null);

  const [loading, setLoading] = useState(true);

  /**
   * Fetch dashboard data.
   */
  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await getDashboard();

		console.log("Dashboard Response:", response);

        /**
         * Backend returns:
         * {
         *   success,
         *   message,
         *   data
         * }
         */
        setDashboard(response.data);

      } catch (error) {
        console.error("Dashboard Error:", error);

      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <ProtectedRoute>
        <DashboardSkeleton />
      </ProtectedRoute>
    );
  }

  if (!dashboard) {
    return (
      <ProtectedRoute>
        <main className="flex min-h-screen items-center justify-center">
          <p>Unable to load dashboard.</p>
        </main>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <main className="min-h-screen bg-slate-50">
        <div className="mx-auto max-w-[1600px] px-4 py-6 sm:px-6 lg:px-8">

        {/* ==========================================================================
            Dashboard Header
        ========================================================================== */}

        <section className="mb-10">
          <h1 className="text-4xl font-bold tracking-tight text-slate-900">
            Dashboard
          </h1>

          <p className="mt-2 text-slate-500">
            Welcome back! Here's what's happening across your farm today.
          </p>
        </section>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
        >
          <Greeting
            fullName={dashboard.farmer.full_name}
          />
        </motion.div>


        <SummaryCards
          totalFarms={dashboard.statistics.total_farms}
          profileCompleted={dashboard.statistics.profile_completed}
          completionPercentage={
            dashboard.statistics.completion_percentage
          }
          registeredDays={dashboard.statistics.registered_days}
        />

        <section
          className="
            mt-6
            grid
            gap-6
            grid-cols-1
            lg:grid-cols-2
          "
        >
          <WeatherCard
            temperature={dashboard.weather.temperature}
            humidity={dashboard.weather.humidity}
            windSpeed={dashboard.weather.wind_speed}
            rainfall={dashboard.weather.rainfall}
            condition={dashboard.weather.condition}
            provider={dashboard.weather.provider}
        />

          <FarmSummaryCard
            farmName={dashboard.primary_farm.farm_name}
            village={dashboard.primary_farm.village}
            district={dashboard.primary_farm.district}
            state={dashboard.primary_farm.state}
            soilType={dashboard.farms[0].soil_type}
            landArea={dashboard.farms[0].land_area}
            landUnit={dashboard.farms[0].land_unit}
            totalFarms={dashboard.statistics.total_farms}
          />
        </section>

        <QuickActions />

        <RecentActivity />

          </div>
      </main>
    </ProtectedRoute>
  );
}