"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";

import {
    LayoutDashboard,
    Sprout,
    CloudSun,
    Bug,
    Wheat,
    Settings,
    LogOut,
} from "lucide-react";

import { cn } from "@/lib/utils";
import { logout } from "@/services/auth.service";

// ============================================================================
// Navigation — every entry here MUST correspond to a real page route.
// Previously included /farmers and /marketplace, which had no matching
// page files and were dead links. /assistant removed from here entirely —
// AI Assistant is now a floating widget (FloatingChatWidget.tsx) mounted
// globally in AuthenticatedLayout, not a page you navigate to.
// ============================================================================

const navigation = [
    { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { label: "Crop Recommendation", href: "/crop-recommendation", icon: Wheat },
    { label: "Disease Detection", href: "/disease-detection", icon: Bug },
    { label: "Weather", href: "/weather", icon: CloudSun },
    // { label: "Settings", href: "/settings", icon: Settings },
    // ^ uncomment once /settings page exists — currently no matching route
];

export default function Sidebar() {
    const pathname = usePathname();
    const router = useRouter();
    const [loggingOut, setLoggingOut] = useState(false);

    const handleLogout = async () => {
        if (loggingOut) return;

        setLoggingOut(true);

        try {
            await logout();
        } finally {
            router.push("/login");
        }
    };

    return (
        <aside className="flex h-screen w-64 flex-shrink-0 flex-col border-r shadow-sm bg-white">
            <div className="border-b px-6 py-5">
                <Link href="/" className="text-2xl font-bold text-green-600">
                    VerdiGO AI
                </Link>
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
                                "flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200",
                                active
                                    ? "bg-green-600 text-white shadow-sm"
                                    : "text-gray-600 hover:bg-green-50 hover:text-green-700"
                            )}
                        >
                            <Icon className="h-5 w-5" />
                            {item.label}
                        </Link>
                    );
                })}
            </nav>

            <div className="border-t p-4">
                <button
                    onClick={handleLogout}
                    disabled={loggingOut}
                    className="flex w-full items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-red-600 transition-colors hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-50"
                >
                    <LogOut className="h-5 w-5" />
                    {loggingOut ? "Logging out..." : "Logout"}
                </button>
            </div>
        </aside>
    );
}