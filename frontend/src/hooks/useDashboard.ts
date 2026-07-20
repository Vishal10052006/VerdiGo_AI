/**
 * ============================================================================
 * useDashboard Hook
 * ============================================================================
 *
 * Encapsulates dashboard data fetching, loading, and error state
 * so the page component stays purely presentational.
 *
 * Module:
 * Phase 1 → Module 4/6 → Dashboard
 * ============================================================================
 */

"use client";

import { useEffect, useState } from "react";

import { getDashboard } from "@/services/dashboard.service";
import type { DashboardResponse } from "@/types/dashboard";

interface UseDashboardResult {
  dashboard: DashboardResponse | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useDashboard(): UseDashboardResult {
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    let cancelled = false;

    const fetchDashboard = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await getDashboard();

        if (!cancelled) {
          setDashboard(response.data);
        }
      } catch (err) {
        console.error("Dashboard fetch error:", err);

        if (!cancelled) {
          setError("Unable to load dashboard. Please try again.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchDashboard();

    return () => {
      cancelled = true;
    };
  }, [refreshKey]);

  const refetch = () => setRefreshKey((key) => key + 1);

  return { dashboard, loading, error, refetch };
}