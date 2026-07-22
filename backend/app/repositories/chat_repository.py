# backend/app/repositories/chat_repository.py
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.chat import ChatConversation, ChatMessage


def create_conversation(db: Session, conversation: ChatConversation) -> ChatConversation:
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation_for_farmer(
    db: Session, conversation_id: UUID, farmer_profile_id: UUID
) -> ChatConversation | None:
    """Ownership-scoped lookup — same 404-not-403 pattern as farm_repository."""
    return (
        db.query(ChatConversation)
        .filter(
            ChatConversation.id == conversation_id,
            ChatConversation.farmer_profile_id == farmer_profile_id,
        )
        .first()
    )


def get_conversations_for_farmer(db: Session, farmer_profile_id: UUID) -> list[ChatConversation]:
    return (
        db.query(ChatConversation)
        .filter(ChatConversation.farmer_profile_id == farmer_profile_id)
        .order_by(ChatConversation.updated_at.desc())
        .all()
    )


def create_message(db: Session, message: ChatMessage) -> ChatMessage:
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_recent_messages(db: Session, conversation_id: UUID, limit: int) -> list[ChatMessage]:
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(messages))  # chronological order for prompt context


def get_all_messages(db: Session, conversation_id: UUID) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )