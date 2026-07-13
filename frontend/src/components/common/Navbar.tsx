/**
 * ============================================================================
 * Navbar Component
 * ============================================================================
 *
 * Description:
 * Shared navigation bar used across VerdiGO.
 *
 * Module:
 * Phase 1 → Module 2 → Task 7
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import Link from "next/link";
import { Bell, UserCircle } from "lucide-react";

import { Button } from "@/components/ui/button";

const navigation = [
    {
        label: "Home",
        href: "/",
    },
    {
        label: "Weather",
        href: "/weather",
    },
    {
        label: "Marketplace",
        href: "/marketplace",
    },
    {
        label: "AI Assistant",
        href: "/assistant",
    },
];

export default function Navbar() {
    return (
        <header className="border-b bg-white">
            <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">

                {/* Logo */}

                <Link
                    href="/"
                    className="text-2xl font-bold text-green-600"
                >
                    VerdiGO AI
                </Link>

                {/* Navigation */}

                <nav className="hidden items-center gap-8 md:flex">
                    {navigation.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className="text-sm font-medium text-gray-600 transition-colors hover:text-green-600"
                        >
                            {item.label}
                        </Link>
                    ))}
                </nav>

                {/* Right Section */}

                <div className="flex items-center gap-2">

                    <Button
                        variant="ghost"
                        size="icon"
                    >
                        <Bell className="h-5 w-5" />
                    </Button>

                    <Button
                        variant="ghost"
                        size="icon"
                    >
                        <UserCircle className="h-6 w-6" />
                    </Button>

                </div>

            </div>
        </header>
    );
}