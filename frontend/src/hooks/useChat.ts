/**
 * ============================================================================
 * useChat Hook
 * ============================================================================
 *
 * Encapsulates chat conversation state: sending messages, optimistic
 * UI updates, error handling (including 429 rate limit), and loading
 * an existing conversation's history.
 *
 * Design note: messages are appended optimistically on send so the
 * UI feels instant. If the request fails, the optimistic user message
 * stays (so the farmer doesn't lose what they typed) but an error
 * message is attached instead of an assistant reply.
 *
 * Module:
 * Phase 1 → Module 7 → AI Chat Assistant
 * ============================================================================
 */

"use client";

import { useCallback, useState } from "react";
import { AxiosError } from "axios";

import { sendChatMessage, getChatHistory } from "@/services/chat.service";
import type { ChatMessage } from "@/types/chat";

interface UseChatResult {
  messages: ChatMessage[];
  conversationId: string | null;
  sending: boolean;
  error: string | null;
  rateLimited: boolean;
  sendMessage: (text: string) => Promise<void>;
  loadConversation: (id: string) => Promise<void>;
  startNewConversation: () => void;
}

const RATE_LIMIT_STATUS = 429;

export function useChat(): UseChatResult {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [rateLimited, setRateLimited] = useState(false);

  const sendMessage = useCallback(
    async (text: string) => {
      const trimmed = text.trim();

      if (!trimmed || sending) {
        return;
      }

      setError(null);
      setRateLimited(false);
      setSending(true);

      // Optimistic user message — shows immediately, before the
      // network round-trip completes.
      const optimisticMessage: ChatMessage = {
        id: `optimistic-${Date.now()}`,
        role: "user",
        content: trimmed,
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, optimisticMessage]);

      try {
        const response = await sendChatMessage(
          trimmed,
          conversationId ?? undefined
        );

        setConversationId(response.conversation_id);

        // Replace optimistic message with real data + append assistant reply.
        setMessages((prev) => [
          ...prev.filter((m) => m.id !== optimisticMessage.id),
          { ...optimisticMessage, id: `user-${response.message.id}` },
          response.message,
        ]);
      } catch (err) {
        console.error("Chat send error:", err);

        const axiosError = err as AxiosError<{ message?: string; detail?: string }>;
        const status = axiosError.response?.status;

        if (status === RATE_LIMIT_STATUS) {
          setRateLimited(true);
          setError(
            axiosError.response?.data?.detail ??
              "You've reached today's message limit. Please try again tomorrow."
          );
        } else if (status === 502 || status === 503) {
          setError(
            "The AI assistant is temporarily unavailable. Please try again shortly."
          );
        } else {
          setError("Unable to send message. Please try again.");
        }

        // Keep the optimistic user message — the farmer's input isn't lost —
        // but don't fabricate an assistant reply.
      } finally {
        setSending(false);
      }
    },
    [conversationId, sending]
  );

  const loadConversation = useCallback(async (id: string) => {
    setError(null);

    try {
      const history = await getChatHistory(id);
      setConversationId(history.conversation_id);
      setMessages(history.messages);
    } catch (err) {
      console.error("Chat history fetch error:", err);
      setError("Unable to load conversation.");
    }
  }, []);

  const startNewConversation = useCallback(() => {
    setConversationId(null);
    setMessages([]);
    setError(null);
    setRateLimited(false);
  }, []);

  return {
    messages,
    conversationId,
    sending,
    error,
    rateLimited,
    sendMessage,
    loadConversation,
    startNewConversation,
  };
}
