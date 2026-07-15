"use client";

import { useEffect, useState } from "react";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import Greeting from "@/components/dashboard/Greeting";

import { getDashboard } from "@/services/dashboard.service";

import SummaryCards from "@/components/dashboard/SummaryCards";

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
        <main className="flex min-h-screen items-center justify-center">
          <p className="text-lg">Loading dashboard...</p>
        </main>
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
      <main className="min-h-screen bg-slate-50 p-8">

        <Greeting
          fullName={dashboard.farmer.full_name}
        />

        <SummaryCards
          totalFarms={dashboard.statistics.total_farms}
          profileCompleted={dashboard.statistics.profile_completed}
          completionPercentage={
            dashboard.statistics.completion_percentage
          }
          registeredDays={dashboard.statistics.registered_days}
        />

      </main>
    </ProtectedRoute>
  );
}