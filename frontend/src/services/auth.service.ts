/**
 * ============================================================================
 * Authentication Service
 * ============================================================================
 *
 * Handles all authentication API requests.
 *
 * Module:
 * Phase 1 → Module 5 → Authentication
 *
 * Backend:
 * FastAPI
 *
 * ============================================================================
 */

import api from "@/lib/api";

/**
 * Send OTP
 */
export const sendOTP = async (mobile: string) => {
  const response = await api.post("/auth/send-otp", {
    mobile,
  });

  return response.data;
};

/**
 * Verify OTP
 */
export const verifyOTP = async (
  mobile: string,
  otp: string
) => {
  const response = await api.post("/auth/verify-otp", {
    mobile,
    otp,
  });

  return response.data;
};

/**
 * Logout
 */
export const logout = async () => {
  const response = await api.post("/auth/logout");

  return response.data;
};

/**
 * Refresh Token
 */
export const refreshToken = async (
  refresh_token: string
) => {
  const response = await api.post("/auth/refresh", {
    refresh_token,
  });

  return response.data;
};

/**
 * Current User
 */
export const getMe = async () => {
  const response = await api.get("/auth/me");

  return response.data;
};