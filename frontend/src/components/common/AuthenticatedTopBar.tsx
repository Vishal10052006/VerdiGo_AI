/**
 * ============================================================================
 * Authenticated Top Bar
 * ============================================================================
 *
 * Thin header shown above page content within AuthenticatedLayout.
 * Currently just houses the notification bell — previously
 * NotificationBadge.tsx existed as a built, tested component with zero
 * call sites anywhere in the app. This is that missing call site.
 *
 * Module:
 * Phase 1 → Module 9 → Notifications
 * ============================================================================
 */

"use client";

import { useRouter } from "next/navigation";

import NotificationBadge from "@/components/notifications/NotificationBadge";
import { useNotifications } from "@/hooks/useNotifications";

export default function AuthenticatedTopBar() {
    const router = useRouter();
    const { unreadCount } = useNotifications();

    return (
        <header className="flex h-16 items-center justify-end border-b bg-white px-6">
            <NotificationBadge
                count={unreadCount}
                onClick={() => router.push("/notifications")}
            />
        </header>
    );
}