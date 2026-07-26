/**
 * ============================================================================
 * Farmer Profile Service
 * ============================================================================
 */

import api from "@/lib/api";

export interface FarmerProfilePayload {
  full_name: string;
  age: number;
  gender: "Male" | "Female" | "Other";
  state: string;
  district: string;
  village: string;
}

export const getFarmerProfile = async () => {
  const response = await api.get("/farmer/profile");
  return response.data;
};

export const createFarmerProfile = async (payload: FarmerProfilePayload) => {
  const response = await api.post("/farmer/profile", payload);
  return response.data;
};
