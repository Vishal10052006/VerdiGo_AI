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
 *
 * Module:
 * Phase 1 → Module 5 → Authentication
 * ============================================================================
 */

import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,

  headers: {
    "Content-Type": "application/json",
  },

  withCredentials: false,
});

/**
 * ============================================================================
 * Request Interceptor
 * ============================================================================
 *
 * Automatically attaches the access token
 * to every authenticated request.
 */
api.interceptors.request.use((config) => {
  console.log("🚀 Interceptor executed");

  const token = localStorage.getItem("access_token");
  console.log("Token:", token);

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log("Header:", config.headers.Authorization);
  }

  return config;
});

export default api;