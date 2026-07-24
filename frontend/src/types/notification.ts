export type NotificationType = "weather" | "disease" | "crop" | "system" | "general";
export type NotificationSeverity = "info" | "low" | "moderate" | "high" | "critical";

export interface Notification {
  id: string;
  type: NotificationType;
  severity: NotificationSeverity;
  title: string;
  message: string;
  related_entity_id: string | null;
  related_entity_type: string | null;
  is_read: boolean;
  created_at: string;
}

export interface NotificationListResponse {
  notifications: Notification[];
  unread_count: number;
}