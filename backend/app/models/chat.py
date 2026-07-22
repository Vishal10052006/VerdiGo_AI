# backend/app/models/chat.py
"""
Chat Models

Stores AI chat conversations and messages between
farmers and the VerdiGO AI Assistant.

Module:
Phase 1 → Module 7 → AI Chat Assistant

Author: VerdiGO Backend Team
"""

import uuid

from sqlalchemy import (
    Column, DateTime, Enum, ForeignKey, Integer,
    String, Text, Boolean, Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.chat import ChatRoleEnum, ChatIntentEnum, AIProviderEnum


class ChatConversation(Base):
    __tablename__ = "chat_conversations"

    __table_args__ = (
        Index("idx_chat_conv_farmer", "farmer_profile_id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    farmer_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("farmer_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(String(150), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    messages = relationship(
        "ChatMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at",
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    __table_args__ = (
        Index("idx_chat_msg_conversation", "conversation_id"),
        Index("idx_chat_msg_created", "created_at"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    role = Column(Enum(ChatRoleEnum), nullable=False)
    content = Column(Text, nullable=False)

    intent = Column(Enum(ChatIntentEnum), nullable=True)
    ai_provider = Column(Enum(AIProviderEnum), nullable=True)

    tokens_used = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversation = relationship("ChatConversation", back_populates="messages")