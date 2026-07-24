// frontend/src/components/admin/AdminProtectedRoute.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isAdminAuthenticated } from "@/lib/adminAuth";

export default function AdminProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [authenticated, setAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const loggedIn = isAdminAuthenticated();
    if (!loggedIn) router.replace("/admin/login");
    setAuthenticated(loggedIn);
  }, [router]);

  if (!authenticated) return null;
  return <>{children}</>;
}