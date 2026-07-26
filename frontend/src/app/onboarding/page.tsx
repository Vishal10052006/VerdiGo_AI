"use client";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import OnboardingForm from "@/components/onboarding/OnboardingForm";

export default function OnboardingPage() {
  return (
    <ProtectedRoute>
      <section className="flex min-h-screen items-center justify-center bg-gradient-to-br from-emerald-50 via-white to-green-50 px-6 py-16">
        <div className="w-full max-w-2xl rounded-3xl border bg-white p-10 shadow-xl">
          <h1 className="text-3xl font-bold">Complete Your Profile</h1>
          <p className="mt-2 text-slate-600">
            Tell us a bit about yourself so we can personalize your farming
            recommendations.
          </p>

          <div className="mt-8">
            <OnboardingForm />
          </div>
        </div>
      </section>
    </ProtectedRoute>
  );
}
