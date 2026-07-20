/**
 * ============================================================================
 * Dashboard Types
 * ============================================================================
 *
 * Shared type contracts for the Dashboard module.
 * Mirrors the backend's DashboardDataSchema response shape.
 *
 * Module:
 * Phase 1 → Module 4/6 → Dashboard
 * ============================================================================
 */

export interface DashboardFarmer {
  full_name: string;
}

export interface DashboardStatistics {
  total_farms: number;
  profile_completed: boolean;
  completion_percentage: number;
  registered_days: number;
}

export interface DashboardWeather {
  temperature: number;
  humidity: number;
  wind_speed: number;
  rainfall: number;
  condition: string;
  provider: string;
}

export interface DashboardPrimaryFarm {
  farm_name: string;
  village: string;
  district: string;
  state: string;
}

export interface DashboardFarm {
  land_area: string;
  land_unit: string;
  soil_type: string;
}

export interface DashboardResponse {
  farmer: DashboardFarmer;
  statistics: DashboardStatistics;
  weather: DashboardWeather;
  primary_farm: DashboardPrimaryFarm;
  farms: DashboardFarm[];
}