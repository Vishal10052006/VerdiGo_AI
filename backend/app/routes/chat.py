# backend/app/routes/chat.py
"""
Chat Routes

Module:
Phase 1 → Module 7 → AI Chat Assistant
"""

from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.common import SuccessResponse
from app.schemas.chat import (
    ChatMessageRequest,
    SendMessageResponseSchema,
    ChatHistoryResponseSchema,
    ConversationSummarySchema,
)
from app.services.chat_service import ChatService
from app.utils.response import success_response


router = APIRouter(prefix="/v1/chat", tags=["AI Chat"])


@router.post("/message", response_model=SuccessResponse[SendMessageResponseSchema])
def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Send a message to the AI Farming Assistant."""
    service = ChatService(db)

    result = service.send_message(
        user_id=current_user.id,
        conversation_id=request.conversation_id,
        message=request.message,
    )

    return success_response(
        schema=SendMessageResponseSchema,
        data={
            "conversation_id": result["conversation_id"],
            "message": result["message"],
        },
        message="Response generated successfully.",
    )


@router.get(
    "/history/{conversation_id}",
    response_model=SuccessResponse[ChatHistoryResponseSchema],
)
def get_chat_history(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve full message history for a conversation."""
    service = ChatService(db)
    messages = service.get_history(current_user.id, conversation_id)

    return success_response(
        schema=ChatHistoryResponseSchema,
        data={"conversation_id": conversation_id, "messages": messages},
        message="Chat history retrieved successfully.",
    )


@router.get("/conversations", response_model=SuccessResponse[list[ConversationSummarySchema]])
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all conversations for the authenticated farmer."""
    service = ChatService(db)
    conversations = service.list_conversations(current_user.id)

    return success_response(
        schema=ConversationSummarySchema,
        data=[ConversationSummarySchema.model_validate(c) for c in conversations],
        message="Conversations retrieved successfully.",
    )