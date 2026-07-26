/**
 * ============================================================================
 * Post-Login Routing
 * ============================================================================
 *
 * Decides where to send a user immediately after authentication
 * (OTP or Google) succeeds and tokens are already stored.
 *
 * New accounts (no FarmerProfile row yet) go to /onboarding.
 * Existing accounts go straight to /dashboard.
 * ============================================================================
 */

import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import api from "@/lib/api";

export const redirectAfterLogin = async (router: AppRouterInstance) => {
  try {
    await api.get("/farmer/profile");
    router.push("/dashboard");
  } catch (error: any) {
    if (error?.response?.status === 404) {
      router.push("/onboarding");
      return;
    }

    // Any other error (network blip, 500, etc.) — don't block login,
    // let the dashboard's own error state handle it with a Retry button.
    console.error("Profile check failed, defaulting to dashboard:", error);
    router.push("/dashboard");
  }
};
