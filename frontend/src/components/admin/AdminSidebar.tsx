// frontend/src/components/admin/AdminSidebar.tsx
"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LayoutDashboard, Users, LogOut, ShieldCheck } from "lucide-react";
import { cn } from "@/lib/utils";
import { clearAdminSession } from "@/lib/adminAuth";

const navigation = [
  { label: "Dashboard", href: "/admin/dashboard", icon: LayoutDashboard },
  { label: "Farmers", href: "/admin/farmers", icon: Users },
];

export default function AdminSidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    clearAdminSession();
    router.push("/admin/login");
  };

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-slate-800 bg-slate-950">
      <div className="flex items-center gap-2 border-b border-slate-800 px-6 py-5">
        <ShieldCheck className="h-6 w-6 text-emerald-500" />
        <span className="text-lg font-bold text-white">Admin Panel</span>
      </div>

      <nav className="flex-1 space-y-2 p-4">
        {navigation.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors",
                active
                  ? "bg-emerald-600 text-white"
                  : "text-slate-400 hover:bg-slate-800 hover:text-white"
              )}
            >
              <Icon className="h-5 w-5" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-slate-800 p-4">
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-red-400 hover:bg-red-950"
        >
          <LogOut className="h-5 w-5" />
          Logout
        </button>
      </div>
    </aside>
  );
}