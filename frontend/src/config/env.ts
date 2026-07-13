/**
 * ============================================================================
 * Environment Configuration
 * ============================================================================
 *
 * Centralized frontend environment variables.
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

export const ENV = {
  API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL!,
  APP_NAME: process.env.NEXT_PUBLIC_APP_NAME!,
  ENVIRONMENT: process.env.NEXT_PUBLIC_ENV!,
} as const;
