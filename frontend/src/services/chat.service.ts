/**
 * ============================================================================
 * Chat Service
 * ============================================================================
 *
 * Handles all AI Chat Assistant API requests.
 *
 * Module:
 * Phase 1 → Module 7 → AI Chat Assistant
 * ============================================================================
 */

import api from "@/lib/api";
import type {
  SendMessageResponse,
  ChatHistoryResponse,
  ConversationSummary,
} from "@/types/chat";

/**
 * ============================================================================
 * Send Message
 * ============================================================================
 *
 * Sends a message to the AI assistant. Omit conversationId to start
 * a new conversation; pass it to continue an existing one.
 */
export const sendChatMessage = async (
  message: string,
  conversationId?: string
): Promise<SendMessageResponse> => {
  const response = await api.post("/v1/chat/message", {
    message,
    conversation_id: conversationId ?? null,
  });

  return response.data.data;
};

/**
 * ============================================================================
 * Get Chat History
 * ============================================================================
 */
export const getChatHistory = async (
  conversationId: string
): Promise<ChatHistoryResponse> => {
  const response = await api.get(`/v1/chat/history/${conversationId}`);
  return response.data.data;
};

/**
 * ============================================================================
 * List Conversations
 * ============================================================================
 */
export const listConversations = async (): Promise<ConversationSummary[]> => {
  const response = await api.get("/v1/chat/conversations");
  return response.data.data;
};
