// frontend/src/lib/adminAuth.ts
/**
 * ============================================================================
 * Admin Authentication Utilities
 * ============================================================================
 * Deliberately separate localStorage keys from farmer auth (lib/auth.ts)
 * so an admin session and a farmer session can never collide in the
 * same browser.
 * Module: Phase 1 → Module 10 → Admin Panel
 */

const ADMIN_TOKEN_KEY = "admin_access_token";
const ADMIN_USER_KEY = "admin_user";

export const isAdminAuthenticated = (): boolean => {
  if (typeof window === "undefined") return false;
  return !!localStorage.getItem(ADMIN_TOKEN_KEY);
};

export const getAdminToken = (): string | null => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ADMIN_TOKEN_KEY);
};

export const setAdminSession = (token: string, admin: unknown) => {
  localStorage.setItem(ADMIN_TOKEN_KEY, token);
  localStorage.setItem(ADMIN_USER_KEY, JSON.stringify(admin));
};

export const clearAdminSession = () => {
  localStorage.removeItem(ADMIN_TOKEN_KEY);
  localStorage.removeItem(ADMIN_USER_KEY);
};