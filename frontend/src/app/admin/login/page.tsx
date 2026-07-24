// frontend/src/app/admin/login/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { ShieldCheck } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { adminLogin } from "@/services/admin.service";
import { setAdminSession } from "@/lib/adminAuth";

export default function AdminLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      toast.warning("Enter email and password.");
      return;
    }

    try {
      setLoading(true);
      const response = await adminLogin(email, password);
      setAdminSession(response.access_token, response.admin);
      toast.success("Welcome back.");
      router.push("/admin/dashboard");
    } catch (error) {
      console.error(error);
      toast.error("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="flex min-h-screen items-center justify-center bg-slate-950 px-6">
      <div className="w-full max-w-md rounded-3xl border border-slate-800 bg-slate-900 p-10 shadow-2xl">
        <div className="mb-8 flex items-center gap-3">
          <div className="rounded-xl bg-emerald-600 p-3">
            <ShieldCheck className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">VerdiGO Admin</h1>
            <p className="text-sm text-slate-400">Sign in to the control panel</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="space-y-2">
            <Label className="text-slate-300">Email</Label>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@verdigo.ai"
              className="bg-slate-800 text-white"
            />
          </div>

          <div className="space-y-2">
            <Label className="text-slate-300">Password</Label>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="bg-slate-800 text-white"
            />
          </div>

          <Button type="submit" disabled={loading} className="w-full rounded-xl py-6">
            {loading ? "Signing in..." : "Sign In"}
          </Button>
        </form>
      </div>
    </section>
  );
}