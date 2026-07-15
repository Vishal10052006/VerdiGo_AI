/**
 * ============================================================================
 * Dashboard Service
 * ============================================================================
 *
 * Handles all Dashboard API requests.
 *
 * Module:
 * Phase 1 → Module 6 → User Dashboard
 *
 * Author: VerdiGO Frontend Team
 * ============================================================================
 */

import api from "@/lib/api";

/**
 * ============================================================================
 * Get Dashboard Summary
 * ============================================================================
 *
 * Fetches complete dashboard information for
 * the authenticated farmer.
 */
export const getDashboard = async () => {
  const response = await api.get("/dashboard");

  return response.data;
};

/**
 * ============================================================================
 * Get Farmer Overview
 * ============================================================================
 */
export const getFarmerOverview = async () => {
  const response = await api.get("/dashboard/overview");

  return response.data;
};