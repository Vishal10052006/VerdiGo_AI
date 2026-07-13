/**
 * ============================================================================
 * Sidebar Component
 * ============================================================================
 *
 * Description:
 * Shared dashboard sidebar for VerdiGO.
 *
 * Module:
 * Phase 1 → Module 2 → Task 8
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import {
    LayoutDashboard,
    Users,
    Sprout,
    CloudSun,
    Bot,
    ShoppingBag,
    Settings,
    LogOut,
} from "lucide-react";

import { cn } from "@/lib/utils";

const navigation = [
    {
        label: "Dashboard",
        href: "/dashboard",
        icon: LayoutDashboard,
    },
    {
        label: "Farmers",
        href: "/farmers",
        icon: Users,
    },
    {
        label: "Farms",
        href: "/farms",
        icon: Sprout,
    },
    {
        label: "Weather",
        href: "/weather",
        icon: CloudSun,
    },
    {
        label: "AI Assistant",
        href: "/assistant",
        icon: Bot,
    },
    {
        label: "Marketplace",
        href: "/marketplace",
        icon: ShoppingBag,
    },
    {
        label: "Settings",
        href: "/settings",
        icon: Settings,
    },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="flex h-screen w-72 flex-col border-r shadow-sm bg-white">

            {/* Logo */}

            <div className="border-b px-6 py-5">
                <Link
                    href="/"
                    className="text-2xl font-bold text-green-600"
                >
                    VerdiGO AI
                </Link>
            </div>

            {/* Navigation */}

            <nav className="flex-1 space-y-3 p-4">

                {navigation.map((item) => {
                    const Icon = item.icon;

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200",
                                pathname === item.href
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

            {/* Logout */}

            <div className="border-t p-4">

                <button
                    className="
                        flex
                        w-full
                        items-center
                        gap-3
                        rounded-lg
                        px-4
                        py-3
                        text-sm
                        font-medium
                        text-red-600
                        transition-colors
                        hover:bg-red-50
                    "
                >
                    <LogOut className="h-5 w-5" />

                    Logout
                </button>

            </div>

        </aside>
    );
}