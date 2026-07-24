import { Bell } from "lucide-react";

interface NotificationBadgeProps {
  count: number;
  onClick?: () => void;
}

export default function NotificationBadge({ count, onClick }: NotificationBadgeProps) {
  return (
    <button onClick={onClick} className="relative rounded-full p-2 hover:bg-gray-100">
      <Bell className="h-5 w-5 text-gray-600" />
      {count > 0 && (
        <span className="absolute -right-0.5 -top-0.5 flex h-4 min-w-[16px] items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-bold text-white">
          {count > 99 ? "99+" : count}
        </span>
      )}
    </button>
  );
}