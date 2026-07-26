/**
 * ============================================================================
 * Onboarding Page
 * ============================================================================
 *
 * Shown to any authenticated user who does not yet have a farmer
 * profile (first-time login, whether via OTP or Google).
 *
 * Route: /onboarding
 * ============================================================================
 */

"use client";

import { Leaf } from "lucide-react";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import OnboardingForm from "@/components/onboarding/OnboardingForm";

export default function OnboardingPage() {
  return (
    <ProtectedRoute>
      <section className="flex min-h-screen items-center justify-center bg-gradient-to-br from-emerald-50 via-white to-green-50 px-6 py-16">
        <div className="w-full max-w-xl rounded-3xl border bg-white p-10 shadow-xl">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-700">
            <Leaf className="h-4 w-4" />
            One Last Step
          </div>

          <h1 className="mb-2 text-3xl font-bold">Complete Your Profile</h1>
          <p className="mb-8 text-slate-600">
            Tell us a bit about yourself and your farm's location so we can
            personalize your VerdiGO experience.
          </p>

          <OnboardingForm />
        </div>
      </section>
    </ProtectedRoute>
  );
}
