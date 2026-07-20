/**
 * ============================================================================
 * Login Page
 * ============================================================================
 *
 * Route: /login
 *
 * Renders the phone + OTP login flow.
 * Redirects to /dashboard if the user is already authenticated.
 *
 * Module:
 * Phase 1 → Module 1 → Authentication
 * ============================================================================
 */

"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import Login from "@/components/auth/Login";
import { isAuthenticated } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.replace("/dashboard");
    }
  }, [router]);

  return <Login />;
}