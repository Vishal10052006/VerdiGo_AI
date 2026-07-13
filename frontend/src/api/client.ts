/**
 * ============================================================================
 * Axios API Client
 * ============================================================================
 *
 * Description:
 * Centralized Axios instance used throughout the VerdiGO frontend
 * for communicating with the backend API.
 *
 * Responsibilities:
 * - Configure API Base URL
 * - Set request timeout
 * - Apply default headers
 * - Serve as the foundation for future JWT interceptors
 * - Centralize all backend communication
 *
 * Module:
 * Phase 1 → Module 1 → Frontend Foundation & Architecture
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import axios from "axios";
import { ENV } from "@/config/env";

/**
 * Shared Axios Client
 */
export const apiClient = axios.create({
  baseURL: ENV.API_BASE_URL,

  timeout: 10000,

  headers: {
    "Content-Type": "application/json",
  },
});
