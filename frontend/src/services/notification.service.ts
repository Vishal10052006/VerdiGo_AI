import api from "@/lib/api";
import type { Notification, NotificationListResponse } from "@/types/notification";

export const getNotifications = async (
  unreadOnly = false
): Promise<NotificationListResponse> => {
  const response = await api.get("/v1/notifications", {
    params: { unread_only: unreadOnly },
  });
  return response.data.data;
};

export const getUnreadCount = async (): Promise<number> => {
  const response = await api.get("/v1/notifications/unread-count");
  return response.data.data.unread_count;
};

export const markNotificationRead = async (id: string): Promise<Notification> => {
  const response = await api.patch(`/v1/notifications/${id}/read`);
  return response.data.data;
};

export const markAllNotificationsRead = async (): Promise<number> => {
  const response = await api.patch("/v1/notifications/read-all");
  return response.data.data.marked_count;
};