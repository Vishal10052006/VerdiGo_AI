"use client";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import { PageHeader } from "@/components/common/PageHeader";
import { EmptyState } from "@/components/common/EmptyState";
import { LoadingSkeleton } from "@/components/common/LoadingSkeleton";
import AlertCard from "@/components/notifications/AlertCard";
import { useNotifications } from "@/hooks/useNotifications";
import { Bell, CheckCheck } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function NotificationsPage() {
  const { notifications, unreadCount, loading, markRead, markAllRead } = useNotifications();

  return (
    <ProtectedRoute>
      <main className="min-h-screen bg-slate-50">
        <PageHeader
          title="Notifications"
          description={`${unreadCount} unread`}
          icon={<Bell className="h-6 w-6" />}
          actionLabel={unreadCount > 0 ? "Mark all read" : undefined}
          onAction={markAllRead}
        />

        <div className="mx-auto max-w-3xl space-y-3 px-4 py-6 sm:px-6 lg:px-8">
          {loading ? (
            <LoadingSkeleton variant="list" />
          ) : notifications.length === 0 ? (
            <EmptyState
              title="No notifications yet"
              description="Weather and disease alerts for your farm will appear here."
              icon={<Bell className="h-10 w-10" />}
            />
          ) : (
            notifications.map((n) => (
              <AlertCard key={n.id} notification={n} onMarkRead={markRead} />
            ))
          )}
        </div>
      </main>
    </ProtectedRoute>
  );
}