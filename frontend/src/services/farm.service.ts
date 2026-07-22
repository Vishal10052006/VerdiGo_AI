/**
 * ============================================================================
 * Farm Service
 * ============================================================================
 *
 * Handles all Farm API requests.
 *
 * Module:
 * Phase 1 → Module 2 → Farmer Registration
 * ============================================================================
 */

import api from "@/lib/api";

/**
 * ============================================================================
 * Get Farm
 * ============================================================================
 *
 * Fetches the authenticated farmer's farm.
 * Note: current backend enforces one farm per farmer profile.
 */
export const getFarm = async () => {
  const response = await api.get("/farm");
  return response.data;
};