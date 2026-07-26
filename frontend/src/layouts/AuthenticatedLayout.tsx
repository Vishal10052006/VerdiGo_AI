/**
 * ============================================================================
 * Authenticated Layout
 * ============================================================================
 *
 * Wraps every authenticated page (Dashboard, Crop Recommendation, Disease
 * Detection, Notifications, etc.) with:
 * - Persistent Sidebar navigation
 * - Top bar (notification bell)
 * - Globally-mounted FloatingChatWidget
 *
 * This is the fix for the gap where 6+ working backend features had zero
 * navigation path from the page a farmer actually lands on after login.
 * Previously each authenticated page rendered its own bare <main>, wrapped
 * only in <ProtectedRoute> (auth check, no UI chrome) — meaning Dashboard,
 * Crop Recommendation, and Disease Detection were three visually
 * disconnected islands with no way to move between them except typing
 * a URL directly.
 *
 * Usage: wrap page content with <ProtectedRoute><AuthenticatedLayout>...
 * Auth check stays in ProtectedRoute (separate concern); this layout is
 * purely visual chrome and only makes sense for already-authenticated users.
 *
 * Module:
 * Shared Layout
 * ============================================================================
 */

"use client";

import { ReactNode } from "react";

import Sidebar from "@/components/common/Sidebar";
import AuthenticatedTopBar from "@/components/common/AuthenticatedTopBar";
import FloatingChatWidget from "@/components/chat/FloatingChatWidget";

interface AuthenticatedLayoutProps {
  children: ReactNode;
}

export default function AuthenticatedLayout({
  children,
}: AuthenticatedLayoutProps) {
  return (
    <div className="flex h-screen overflow-hidden bg-slate-50">
      <Sidebar />

      <div className="flex flex-1 flex-col overflow-hidden">
        <AuthenticatedTopBar />

        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>

      <FloatingChatWidget />
    </div>
  );
}