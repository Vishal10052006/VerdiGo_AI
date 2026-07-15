/**
 * ============================================================================
 * Authentication Utilities
 * ============================================================================
 *
 * Handles authentication session helpers.
 *
 * Module:
 * Phase 1 → Module 5 → Authentication
 * ============================================================================
 */

/**
 * Check if user is authenticated.
 */
export const isAuthenticated = (): boolean => {
  if (typeof window === "undefined") {
    return false;
  }

  return !!localStorage.getItem("access_token");
};

/**
 * Get access token.
 */
export const getAccessToken = (): string | null => {
  if (typeof window === "undefined") {
    return null;
  }

  return localStorage.getItem("access_token");
};

/**
 * Clear authentication session.
 */
export const clearSession = () => {
  /**
   * Remove stored session.
   */
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
};