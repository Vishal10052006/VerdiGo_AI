"use client";

import { useCallback, useEffect, useState } from "react";
import {
  getNotifications,
  getUnreadCount,
  markNotificationRead,
  markAllNotificationsRead,
} from "@/services/notification.service";
import type { Notification } from "@/types/notification";

const POLL_INTERVAL_MS = 30_000; // 30s — cheap enough at MVP scale, upgrade to WS later

export function useNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAll = useCallback(async () => {
    try {
      const data = await getNotifications();
      setNotifications(data.notifications);
      setUnreadCount(data.unread_count);
      setError(null);
    } catch (err) {
      console.error("Notification fetch error:", err);
      setError("Unable to load notifications.");
    } finally {
      setLoading(false);
    }
  }, []);

  const pollBadge = useCallback(async () => {
    try {
      const count = await getUnreadCount();
      setUnreadCount(count);
    } catch {
      // Silent — badge polling failures shouldn't surface errors to the user
    }
  }, []);

  useEffect(() => {
    fetchAll();
    const interval = setInterval(pollBadge, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [fetchAll, pollBadge]);

  const markRead = async (id: string) => {
    await markNotificationRead(id);
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
    );
    setUnreadCount((prev) => Math.max(0, prev - 1));
  };

  const markAllRead = async () => {
    await markAllNotificationsRead();
    setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
    setUnreadCount(0);
  };

  return { notifications, unreadCount, loading, error, markRead, markAllRead, refetch: fetchAll };
}