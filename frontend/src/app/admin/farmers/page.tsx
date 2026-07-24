// frontend/src/app/admin/farmers/page.tsx
"use client";

import { useEffect, useState, useCallback } from "react";
import { toast } from "sonner";
import AdminProtectedRoute from "@/components/admin/AdminProtectedRoute";
import AdminSidebar from "@/components/admin/AdminSidebar";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { LoadingSkeleton } from "@/components/common/LoadingSkeleton";
import { getFarmers, updateFarmerStatus } from "@/services/admin.service";

interface FarmerRow {
  user_id: string;
  full_name: string | null;
  mobile: string;
  state: string | null;
  total_farms: number;
  profile_completed: boolean;
  is_active: boolean;
}

export default function AdminFarmersPage() {
  const [farmers, setFarmers] = useState<FarmerRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const pageSize = 20;

  const fetchFarmers = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getFarmers({ page, page_size: pageSize, search: search || undefined });
      setFarmers(data.farmers);
      setTotal(data.total);
    } catch (err) {
      console.error(err);
      toast.error("Unable to load farmers.");
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => {
    fetchFarmers();
  }, [fetchFarmers]);

  const toggleStatus = async (userId: string, current: boolean) => {
    try {
      await updateFarmerStatus(userId, !current);
      toast.success(`Farmer ${!current ? "activated" : "deactivated"}.`);
      fetchFarmers();
    } catch {
      toast.error("Unable to update status.");
    }
  };

  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  return (
    <AdminProtectedRoute>
      <div className="flex min-h-screen bg-slate-950">
        <AdminSidebar />

        <main className="flex-1 p-8">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">Farmers</h1>
              <p className="text-sm text-slate-400">{total} registered farmers</p>
            </div>

            <Input
              placeholder="Search by name or mobile..."
              value={search}
              onChange={(e) => {
                setPage(1);
                setSearch(e.target.value);
              }}
              className="max-w-xs bg-slate-900 text-white"
            />
          </div>

          {loading ? (
            <LoadingSkeleton variant="table" />
          ) : (
            <div className="overflow-hidden rounded-2xl border border-slate-800">
              <table className="w-full text-sm text-slate-300">
                <thead className="bg-slate-900 text-left text-xs uppercase text-slate-500">
                  <tr>
                    <th className="px-4 py-3">Name</th>
                    <th className="px-4 py-3">Mobile</th>
                    <th className="px-4 py-3">State</th>
                    <th className="px-4 py-3">Farms</th>
                    <th className="px-4 py-3">Profile</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {farmers.map((f) => (
                    <tr key={f.user_id} className="border-t border-slate-800">
                      <td className="px-4 py-3 font-medium text-white">{f.full_name ?? "—"}</td>
                      <td className="px-4 py-3">{f.mobile}</td>
                      <td className="px-4 py-3">{f.state ?? "—"}</td>
                      <td className="px-4 py-3">{f.total_farms}</td>
                      <td className="px-4 py-3">
                        <span
                          className={
                            f.profile_completed
                              ? "rounded-full bg-emerald-950 px-2 py-1 text-xs text-emerald-400"
                              : "rounded-full bg-amber-950 px-2 py-1 text-xs text-amber-400"
                          }
                        >
                          {f.profile_completed ? "Complete" : "Incomplete"}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={
                            f.is_active
                              ? "rounded-full bg-emerald-950 px-2 py-1 text-xs text-emerald-400"
                              : "rounded-full bg-red-950 px-2 py-1 text-xs text-red-400"
                          }
                        >
                          {f.is_active ? "Active" : "Inactive"}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Button
                          variant={f.is_active ? "destructive" : "primary"}
                          size="sm"
                          onClick={() => toggleStatus(f.user_id, f.is_active)}
                        >
                          {f.is_active ? "Deactivate" : "Activate"}
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <div className="mt-4 flex items-center justify-between text-sm text-slate-400">
            <span>
              Page {page} of {totalPages}
            </span>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
              >
                Previous
              </Button>
              <Button
                variant="outline"
                size="sm"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
              >
                Next
              </Button>
            </div>
          </div>
        </main>
      </div>
    </AdminProtectedRoute>
  );
}