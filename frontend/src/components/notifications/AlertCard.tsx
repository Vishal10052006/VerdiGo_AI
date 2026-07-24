import { CloudRain, Bug, Sprout, Bell as BellIcon, Info } from "lucide-react";
import type { Notification } from "@/types/notification";
import { cn } from "@/lib/utils";

const TYPE_ICON = { weather: CloudRain, disease: Bug, crop: Sprout, system: BellIcon, general: Info };

const SEVERITY_STYLES: Record<string, string> = {
  info: "border-l-slate-300",
  low: "border-l-yellow-400",
  moderate: "border-l-orange-400",
  high: "border-l-red-400",
  critical: "border-l-red-600",
};

interface AlertCardProps {
  notification: Notification;
  onMarkRead: (id: string) => void;
}

export default function AlertCard({ notification, onMarkRead }: AlertCardProps) {
  const Icon = TYPE_ICON[notification.type] ?? Info;

  return (
    <div
      onClick={() => !notification.is_read && onMarkRead(notification.id)}
      className={cn(
        "flex cursor-pointer items-start gap-4 rounded-xl border-l-4 bg-white p-4 shadow-sm transition hover:shadow-md",
        SEVERITY_STYLES[notification.severity],
        !notification.is_read && "bg-emerald-50/40"
      )}
    >
      <div className="rounded-lg bg-slate-100 p-2">
        <Icon className="h-5 w-5 text-slate-600" />
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between">
          <h4 className="font-semibold text-slate-900">{notification.title}</h4>
          {!notification.is_read && (
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
          )}
        </div>
        <p className="mt-1 text-sm text-slate-600">{notification.message}</p>
        <p className="mt-2 text-xs text-slate-400">
          {new Date(notification.created_at).toLocaleString()}
        </p>
      </div>
    </div>
  );
}