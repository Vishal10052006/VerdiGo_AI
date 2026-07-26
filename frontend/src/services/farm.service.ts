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

export interface FarmPayload {
  farm_name: string;
  land_area: number;
  land_unit: "Acre" | "Hectare" | "Bigha";
  soil_type: string;
  latitude: number;
  longitude: number;
}

/**
 * Get Farm
 *
 * Fetches the authenticated farmer's farm. Backend enforces one farm
 * per farmer profile.
 */
export const getFarm = async () => {
  const response = await api.get("/farm");
  return response.data;
};

/**
 * Create Farm
 */
export const createFarm = async (payload: FarmPayload) => {
  const response = await api.post("/farm", payload);
  return response.data;
};

/**
 * Update Farm (partial — only send fields that changed)
 */
export const updateFarm = async (payload: Partial<FarmPayload>) => {
  const response = await api.put("/farm", payload);
  return response.data;
};