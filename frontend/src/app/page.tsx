"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import LandingPage from "@/components/landing/LandingPage";
import { isAuthenticated } from "@/lib/auth";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.replace("/dashboard");
    }
  }, [router]);

  return <LandingPage />;
}