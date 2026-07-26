/**
 * ============================================================================
 * Axios API Client
 * ============================================================================
 *
 * Centralized Axios instance for VerdiGO.
 *
 * Responsibilities:
 * - Base URL
 * - JSON requests
 * - Automatically attach JWT Access Token
 * - Automatically refresh an expired access token and retry the
 *   original request (fixes the "dashboard breaks after ~15-30 min"
 *   bug — previously a 401 from an expired access token had no
 *   recovery path and just surfaced as a generic error to the user)
 *
 * Module:
 * Phase 1 → Module 5 → Authentication
 * ============================================================================
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import {
  getAccessToken,
  getRefreshToken,
  clearSession,
} from "@/lib/auth";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: false,
});

// ============================================================================
// Request Interceptor — attach access token
// ============================================================================

api.interceptors.request.use((config) => {
  const token = getAccessToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// ============================================================================
// Response Interceptor — auto-refresh on 401
//
// FIX: previously a 401 (expired access token — happens automatically
// every ACCESS_TOKEN_EXPIRE_MINUTES, ~15-30 min) had no recovery path.
// This is the exact cause of "dashboard breaks every 15-20 minutes" —
// the refresh token + refreshToken() service function already existed
// but were never wired into the actual request pipeline.
//
// `isRefreshing` + `pendingQueue` prevent a thundering-herd problem:
// if 4 API calls all 401 at once (e.g. dashboard's parallel fetches),
// only ONE refresh request fires; the other 3 wait for it and retry
// with the new token once it resolves.
// ============================================================================

let isRefreshing = false;
let pendingQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
}> = [];

function resolveQueue(token: string) {
  pendingQueue.forEach(({ resolve }) => resolve(token));
  pendingQueue = [];
}

function rejectQueue(error: unknown) {
  pendingQueue.forEach(({ reject }) => reject(error));
  pendingQueue = [];
}

interface RetryableConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as RetryableConfig | undefined;

    // Not a 401, or no config to retry, or already retried once — give up.
    if (
      !originalRequest ||
      error.response?.status !== 401 ||
      originalRequest._retry
    ) {
      return Promise.reject(error);
    }

    // Don't attempt to refresh on the refresh/login endpoints themselves
    // — avoids an infinite loop if the refresh token is ALSO invalid.
    const skipRefreshPaths = ["/auth/refresh", "/auth/login", "/auth/verify-otp"];
    if (skipRefreshPaths.some((path) => originalRequest.url?.includes(path))) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    const refreshTokenValue = getRefreshToken();

    if (!refreshTokenValue) {
      // No refresh token at all — nothing to do but force re-login.
      clearSession();
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
      return Promise.reject(error);
    }

    if (isRefreshing) {
      // A refresh is already in flight — queue this request and wait.
      return new Promise((resolve, reject) => {
        pendingQueue.push({
          resolve: (newToken: string) => {
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            resolve(api(originalRequest));
          },
          reject,
        });
      });
    }

    isRefreshing = true;

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`,
        { refresh_token: refreshTokenValue }
      );

      const newAccessToken = response.data.access_token;
      localStorage.setItem("access_token", newAccessToken);

      resolveQueue(newAccessToken);

      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
      return api(originalRequest);
    } catch (refreshError) {
      // Refresh token itself is invalid/expired/revoked — genuinely
      // logged out, force back to login rather than looping errors.
      rejectQueue(refreshError);
      clearSession();
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default api;