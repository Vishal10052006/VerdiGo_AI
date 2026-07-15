"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { isAuthenticated } from "@/lib/auth";

/**
 * ============================================================================
 * Protected Route
 * ============================================================================
 *
 * Redirects unauthenticated users
 * to the Login page.
 *
 * Module:
 * Phase 1 → Module 5 → Authentication
 * ============================================================================
 */

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({
  children,
}: ProtectedRouteProps) {
  const router = useRouter();

  const [authenticated, setAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const loggedIn = isAuthenticated();

    if (!loggedIn) {
      router.replace("/");
    }

    setAuthenticated(loggedIn);
  }, [router]);

  // Prevent hydration mismatch and flashing protected content
  if (authenticated === null) {
    return null;
  }

  if (!authenticated) {
    return null;
  }

  return <>{children}</>;
}