// frontend/src/lib/adminApi.ts
/**
 * Separate Axios instance for admin routes — attaches the admin
 * token, not the farmer token. Prevents accidental cross-auth bugs.
 * Module: Phase 1 → Module 10 → Admin Panel
 */
import axios from "axios";
import { getAdminToken, clearAdminSession } from "@/lib/adminAuth";

const adminApi = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: { "Content-Type": "application/json" },
});

adminApi.interceptors.request.use((config) => {
  const token = getAdminToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

adminApi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      clearAdminSession();
      if (typeof window !== "undefined") window.location.href = "/admin/login";
    }
    return Promise.reject(error);
  }
);

export default adminApi;