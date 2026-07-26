/**
 * ============================================================================
 * Post-Login Routing
 * ============================================================================
 *
 * After ANY successful login (OTP or Google), decide where the user
 * should land: /dashboard if they already have a farmer profile,
 * /onboarding if this is their first time (no profile yet).
 *
 * Centralized here so OTP login and Google login can't drift apart
 * on this logic again.
 */

import { AxiosError } from "axios";
import { getFarmerProfile } from "@/services/farmer.service";

export const routeAfterLogin = async (
  router: { push: (path: string) => void }
) => {
  try {
    await getFarmerProfile();
    router.push("/dashboard");
  } catch (error) {
    const axiosError = error as AxiosError;

    if (axiosError.response?.status === 404) {
      router.push("/onboarding");
      return;
    }

    // Any other error (network, 500, etc.) — don't block the user,
    // let them into the dashboard where the existing error state
    // (ErrorState + Retry) already handles failures gracefully.
    router.push("/dashboard");
  }
};
