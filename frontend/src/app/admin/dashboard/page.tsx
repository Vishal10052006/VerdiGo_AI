// frontend/src/app/admin/dashboard/page.tsx
"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Users, Sprout, CheckCircle2, TrendingUp } from "lucide-react";

import AdminProtectedRoute from "@/components/admin/AdminProtectedRoute";
import AdminSidebar from "@/components/admin/AdminSidebar";
import { LoadingSkeleton } from "@/components/common/LoadingSkeleton";
import { getAnalyticsOverview } from "@/services/admin.service";

interface Overview {
  total_farmers: number;
  active_farmers: number;
  total_farms: number;
  profile_completion_rate: number;
  new_farmers_last_7_days: number;
  total_crop_recommendations: number;
  total_disease_detections: number;
  total_chat_messages: number;
  state_distribution: Record<string, number>;
}

export default function AdminDashboardPage() {
  const [data, setData] = useState<Overview | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAnalyticsOverview()
      .then(setData)
      .catch(() => toast.error("Unable to load analytics."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <AdminProtectedRoute>
      <div className="flex min-h-screen bg-slate-950">
        <AdminSidebar />

        <main className="flex-1 p-8">
          <h1 className="mb-6 text-2xl font-bold text-white">Dashboard Analytics</h1>

          {loading || !data ? (
            <LoadingSkeleton variant="card" />
          ) : (
            <>
              <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
                <StatCard icon={<Users className="h-6 w-6" />} label="Total Farmers" value={data.total_farmers} />
                <StatCard icon={<CheckCircle2 className="h-6 w-6" />} label="Active Farmers" value={data.active_farmers} />
                <StatCard icon={<Sprout className="h-6 w-6" />} label="Total Farms" value={data.total_farms} />
                <StatCard
                  icon={<TrendingUp className="h-6 w-6" />}
                  label="New (7 days)"
                  value={data.new_farmers_last_7_days}
                />
              </div>

              <div className="mt-8 grid gap-6 md:grid-cols-3">
                <StatCard label="Profile Completion" value={`${data.profile_completion_rate}%`} />
                <StatCard label="Crop Recommendations" value={data.total_crop_recommendations} />
                <StatCard label="Disease Detections" value={data.total_disease_detections} />
              </div>

              <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <h2 className="mb-4 text-lg font-semibold text-white">Top States</h2>
                <div className="space-y-3">
                  {Object.entries(data.state_distribution).map(([state, count]) => (
                    <div key={state} className="flex items-center justify-between text-sm">
                      <span className="text-slate-300">{state}</span>
                      <span className="font-semibold text-white">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </AdminProtectedRoute>
  );
}

function StatCard({
  icon,
  label,
  value,
}: {
  icon?: React.ReactNode;
  label: string;
  value: string | number;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      {icon && <div className="mb-3 text-emerald-500">{icon}</div>}
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-1 text-3xl font-bold text-white">{value}</p>
    </div>
  );
}