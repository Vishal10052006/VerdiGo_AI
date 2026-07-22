# backend/app/schemas/chat.py
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator

from app.enums.chat import ChatRoleEnum, ChatIntentEnum, AIProviderEnum


class ChatMessageRequest(BaseModel):
    conversation_id: UUID | None = None
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 1:
            raise ValueError("Message cannot be empty.")
        if len(value) > 1000:
            raise ValueError("Message cannot exceed 1000 characters.")
        return value


class ChatMessageResponse(BaseModel):
    id: UUID
    role: ChatRoleEnum
    content: str
    intent: ChatIntentEnum | None = None
    ai_provider: AIProviderEnum | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SendMessageResponseSchema(BaseModel):
    conversation_id: UUID
    message: ChatMessageResponse


class ConversationSummarySchema(BaseModel):
    id: UUID
    title: str | None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatHistoryResponseSchema(BaseModel):
    conversation_id: UUID
    messages: list[ChatMessageResponse]