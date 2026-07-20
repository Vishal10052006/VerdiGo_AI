/**
 * ============================================================================
 * Authentication Service
 * ============================================================================
 */

import api from "@/lib/api";
import { clearSession, getRefreshToken } from "@/lib/auth";

export const sendOTP = async (mobile: string) => {
  const response = await api.post("/auth/send-otp", { mobile });
  return response.data;
};

export const verifyOTP = async (mobile: string, otp: string) => {
  const response = await api.post("/auth/verify-otp", { mobile, otp });
  return response.data;
};

/**
 * Logout
 *
 * Calls the server to revoke the refresh token and blacklist
 * the current access token, THEN clears local session state.
 *
 * Session is cleared even if the API call fails (network issue,
 * token already expired, etc.) — the user must never get stuck
 * unable to log out on the client.
 */
export const logout = async () => {
  try {
    const refreshToken = getRefreshToken();

    const response = await api.post("/auth/logout", {
      refresh_token: refreshToken,
    });

    return response.data;
  } catch (error) {
    console.error("Server-side logout failed, clearing session anyway:", error);
    return { success: true, message: "Logged out locally." };
  } finally {
    clearSession();
  }
};

export const refreshToken = async (refresh_token: string) => {
  const response = await api.post("/auth/refresh", { refresh_token });
  return response.data;
};

export const getMe = async () => {
  const response = await api.get("/auth/me");
  return response.data;
};