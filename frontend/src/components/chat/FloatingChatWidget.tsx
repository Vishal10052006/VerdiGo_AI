/**
 * ============================================================================
 * Floating Chat Widget
 * ============================================================================
 *
 * Intercom-style floating action button (bottom-right) that expands into
 * a compact chat panel. Mounted once in AuthenticatedLayout so it's
 * available on every authenticated page — dashboard, crop recommendation,
 * disease detection, etc. — without needing a dedicated nav link.
 *
 * Deliberately hides itself on the standalone /assistant route (if that
 * full-page route is still linked anywhere) to avoid showing two chat
 * UIs stacked on top of each other.
 *
 * Module:
 * Phase 1 → Module 7 → AI Chat Assistant
 * ============================================================================
 */

"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import { Bot, X } from "lucide-react";

import ChatWindow from "./ChatWindow";
import { cn } from "@/lib/utils";

export default function FloatingChatWidget() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  // Avoid double chat UI if the full-page /assistant route is ever
  // reached directly (e.g. a bookmarked link, or a future deep-link
  // from a notification).
  if (pathname?.startsWith("/assistant")) {
    return null;
  }

  return (
    <>
      {/* Chat Panel */}
      {open && (
        <div
          className={cn(
            "fixed bottom-24 right-6 z-50",
            "h-[520px] w-[380px] max-w-[calc(100vw-3rem)]",
            "animate-in fade-in slide-in-from-bottom-4 duration-200"
          )}
        >
          <ChatWindow variant="floating" />
        </div>
      )}

      {/* Floating Action Button */}
      <button
        onClick={() => setOpen((prev) => !prev)}
        aria-label={open ? "Close AI Assistant" : "Open AI Assistant"}
        className={cn(
          "fixed bottom-6 right-6 z-50",
          "flex h-14 w-14 items-center justify-center rounded-full",
          "bg-emerald-600 text-white shadow-lg",
          "transition-all duration-200 hover:scale-105 hover:bg-emerald-700",
          "focus:outline-none focus-visible:ring-4 focus-visible:ring-emerald-300"
        )}
      >
        {open ? (
          <X className="h-6 w-6" />
        ) : (
          <Bot className="h-6 w-6" />
        )}
      </button>
    </>
  );
}