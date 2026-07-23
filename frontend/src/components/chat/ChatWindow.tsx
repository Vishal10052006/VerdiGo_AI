/**
 * ============================================================================
 * Chat Window
 * ============================================================================
 *
 * Main chat interface: message list, composer, and status states
 * (sending, error, rate-limited).
 *
 * Module:
 * Phase 1 → Module 7 → AI Chat Assistant
 * ============================================================================
 */

"use client";

import { useEffect, useRef, useState } from "react";
import { Bot, Send, AlertCircle } from "lucide-react";

import { useChat } from "@/hooks/useChat";
import { cn } from "@/lib/utils";
import ChatBubble from "./ChatBubble";

export default function ChatWindow() {
  const {
    messages,
    sending,
    error,
    rateLimited,
    sendMessage,
  } = useChat();

  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || sending || rateLimited) {
      return;
    }

    const text = input;
    setInput("");
    await sendMessage(text);
  };

  return (
    <div className="flex h-[calc(100vh-6rem)] flex-col rounded-3xl border bg-white shadow-sm">
      {/* Header */}
      <div className="flex items-center gap-3 border-b px-6 py-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-100">
          <Bot className="h-5 w-5 text-emerald-600" />
        </div>
        <div>
          <h2 className="font-bold text-slate-900">VerdiGO AI Assistant</h2>
          <p className="text-xs text-slate-500">
            Ask about crops, weather, irrigation & more
          </p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 space-y-4 overflow-y-auto px-6 py-6">
        {messages.length === 0 && (
          <div className="flex h-full flex-col items-center justify-center text-center text-slate-400">
            <Bot className="mb-3 h-10 w-10" />
            <p className="text-sm">
              Ask me anything about your farm — crops, weather, fertilizer, or pests.
            </p>
          </div>
        )}

        {messages.map((message) => (
          <ChatBubble key={message.id} message={message} />
        ))}

        {sending && (
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <span className="flex h-2 w-2 animate-pulse rounded-full bg-emerald-500" />
            VerdiGO is thinking...
          </div>
        )}

        <div ref={scrollRef} />
      </div>

      {/* Error / Rate Limit Banner */}
      {error && (
        <div
          className={cn(
            "mx-6 mb-3 flex items-center gap-2 rounded-xl px-4 py-2 text-sm",
            rateLimited
              ? "bg-amber-50 text-amber-700"
              : "bg-red-50 text-red-600"
          )}
        >
          <AlertCircle className="h-4 w-4 flex-shrink-0" />
          {error}
        </div>
      )}

      {/* Composer */}
      <form
        onSubmit={handleSubmit}
        className="flex items-center gap-3 border-t px-6 py-4"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            rateLimited
              ? "Daily limit reached — try again tomorrow"
              : "Type your question..."
          }
          disabled={sending || rateLimited}
          maxLength={1000}
          className="flex-1 rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-emerald-500 disabled:cursor-not-allowed disabled:bg-slate-50"
        />

        <button
          type="submit"
          disabled={!input.trim() || sending || rateLimited}
          className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-600 text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-40"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
}
