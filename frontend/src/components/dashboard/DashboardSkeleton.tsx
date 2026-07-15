/**
 * ============================================================================
 * Dashboard Skeleton
 * ============================================================================
 *
 * Loading placeholder shown while dashboard data is loading.
 *
 * Responsibilities:
 * - Mimic final dashboard layout
 * - Improve perceived loading performance
 *
 * Module:
 * Phase 1 → Module 6 → Dashboard
 *
 * Author: VerdiGO Frontend Team
 * ============================================================================
 */

export default function DashboardSkeleton() {
  return (
    <main className="min-h-screen bg-slate-50 p-8 animate-pulse">

      {/* Header */}
      <div className="mb-8 h-56 rounded-3xl bg-slate-200" />

      {/* Summary Cards */}
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        {[...Array(4)].map((_, index) => (
          <div
            key={index}
            className="h-36 rounded-3xl bg-slate-200"
          />
        ))}
      </div>

      {/* Weather + Farm */}
      <div className="mt-8 grid gap-6 xl:grid-cols-2">
        <div className="h-80 rounded-3xl bg-slate-200" />
        <div className="h-80 rounded-3xl bg-slate-200" />
      </div>

      {/* Quick Actions */}
      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <div className="h-32 rounded-3xl bg-slate-200" />
        <div className="h-32 rounded-3xl bg-slate-200" />
      </div>

      {/* Recent Activity */}
      <div className="mt-8 h-56 rounded-3xl bg-slate-200" />

    </main>
  );
}