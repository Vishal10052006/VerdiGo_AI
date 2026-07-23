/**
 * ============================================================================
 * AI Assistant Page
 * ============================================================================
 *
 * Route: /assistant
 *
 * Module:
 * Phase 1 → Module 7 → AI Chat Assistant
 * ============================================================================
 */

"use client";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import ChatWindow from "@/components/chat/ChatWindow";

export default function AssistantPage() {
  return (
    <ProtectedRoute>
      <main className="min-h-screen bg-slate-50">
        <div className="mx-auto max-w-4xl px-4 py-6 sm:px-6 lg:px-8">
          <section className="mb-6">
            <h1 className="text-3xl font-bold tracking-tight text-slate-900">
              AI Assistant
            </h1>
            <p className="mt-1 text-slate-500">
              Your 24/7 farming advisor, powered by VerdiGO AI.
            </p>
          </section>

          <ChatWindow />
        </div>
      </main>
    </ProtectedRoute>
  );
}
