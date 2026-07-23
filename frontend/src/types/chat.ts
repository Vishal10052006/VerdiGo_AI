/**
 * ============================================================================
 * Chat Types
 * ============================================================================
 *
 * Mirrors backend/app/schemas/chat.py response shapes.
 *
 * Module:
 * Phase 1 → Module 7 → AI Chat Assistant
 * ============================================================================
 */

export type ChatRole = "user" | "assistant" | "system";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  intent?: string | null;
  ai_provider?: string | null;
  created_at: string;
}

export interface SendMessageResponse {
  conversation_id: string;
  message: ChatMessage;
}

export interface ChatHistoryResponse {
  conversation_id: string;
  messages: ChatMessage[];
}

export interface ConversationSummary {
  id: string;
  title: string | null;
  updated_at: string;
}
