"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import Login from "@/components/auth/Login";
import { isAuthenticated } from "@/lib/auth";

export default function Home() {
  const router = useRouter();

  /**
   * Auto-login.
   *
   * If an access token already exists,
   * redirect the user directly to the dashboard.
   */
  useEffect(() => {
    if (isAuthenticated()) {
      router.replace("/dashboard");
    }
  }, [router]);

  return <Login />;
}