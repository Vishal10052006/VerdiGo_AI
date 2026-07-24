# backend/app/services/chat_service.py
"""
Chat Service

Orchestrates conversation lifecycle, context building,
AI generation, and persistence.

Module:
Phase 1 → Module 7 → AI Chat Assistant

Author: VerdiGO Backend Team
"""

from uuid import UUID
from sqlalchemy.orm import Session

from app.models.chat import ChatConversation, ChatMessage
from app.enums.chat import ChatRoleEnum
from app.repositories import chat_repository, farmer_repository, farm_repository
from app.services.ai.ai_provider_manager import AIProviderManager
from app.services.ai.prompt_builder import build_system_prompt
from app.services.ai.intent_classifier import classify_intent
from app.services.weather_service import WeatherService
from app.services.season_service import SeasonService
from app.core.exceptions import NotFoundException

from app.core.exceptions import NotFoundException, ServiceUnavailableException
from app.core.exceptions import (
    NotFoundException,
    ServiceUnavailableException,
    TooManyRequestsException,
)
from app.repositories import chat_rate_limit_repository
from app.config.settings import settings


MAX_HISTORY_MESSAGES = 10  # sliding window — cost + context-length control


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_manager = AIProviderManager()

    def send_message(
        self,
        user_id: UUID,
        conversation_id: UUID | None,
        message: str,
    ) -> dict:
        # ------------------------------------------------------------
        # Resolve Farmer + Farm Context
        # ------------------------------------------------------------
        farmer_profile = farmer_repository.get_by_user_id(self.db, user_id)
        if farmer_profile is None:
            raise NotFoundException(message="Farmer profile not found.")

        current_count = chat_rate_limit_repository.increment_and_get_count(
            db=self.db,
            farmer_profile_id=farmer_profile.id,
        )

        if current_count > settings.AI_DAILY_MESSAGE_LIMIT:
            raise TooManyRequestsException(
                message=(
                    f"You've reached today's limit of "
                    f"{settings.AI_DAILY_MESSAGE_LIMIT} messages. "
                    f"Please try again tomorrow."
                )
            )

        farm = farm_repository.get_by_farmer_profile_id(self.db, farmer_profile.id)


        # ------------------------------------------------------------
        # Rate Limit Check (cost control — before any AI spend)
        # ------------------------------------------------------------
        current_count = chat_rate_limit_repository.increment_and_get_count(
            db=self.db,
            farmer_profile_id=farmer_profile.id,
        )

        if current_count > settings.AI_DAILY_MESSAGE_LIMIT:
            raise TooManyRequestsException(
                message=(
                    f"You've reached today's limit of "
                    f"{settings.AI_DAILY_MESSAGE_LIMIT} messages. "
                    f"Please try again tomorrow."
                )
            )

        # ------------------------------------------------------------
        # Get or Create Conversation (scoped to this farmer only)
        # ------------------------------------------------------------
        if conversation_id:
            conversation = chat_repository.get_conversation_for_farmer(
                self.db, conversation_id, farmer_profile.id
            )
            if conversation is None:
                raise NotFoundException(message="Conversation not found.")
        else:
            conversation = chat_repository.create_conversation(
                self.db,
                ChatConversation(
                    farmer_profile_id=farmer_profile.id,
                    title=message[:80],
                ),
            )

        # ------------------------------------------------------------
        # Build Context: Weather (best-effort, don't fail chat if down)
        # ------------------------------------------------------------
        weather = None
        if farm:
            try:
                weather = WeatherService(self.db).get_current_weather(
                    farm_id=farm.id, latitude=farm.latitude, longitude=farm.longitude,
                )
            except Exception:
                weather = None  # Chat must degrade gracefully, not fail

        season = SeasonService.get_current_season().value

        system_prompt = build_system_prompt(farmer_profile, farm, weather, season)

        # ------------------------------------------------------------
        # Build Sliding-Window History
        # ------------------------------------------------------------
        history_messages = chat_repository.get_recent_messages(
            self.db, conversation.id, limit=MAX_HISTORY_MESSAGES,
        )
        history = [
            {"role": m.role.value, "content": m.content}
            for m in history_messages
            if m.role != ChatRoleEnum.SYSTEM
        ]

        # ------------------------------------------------------------
        # Persist User Message
        # ------------------------------------------------------------
        intent = classify_intent(message)

        chat_repository.create_message(
            self.db,
            ChatMessage(
                conversation_id=conversation.id,
                role=ChatRoleEnum.USER,
                content=message,
                intent=intent,
            ),
        )

        # ------------------------------------------------------------
        # Generate AI Response
        # ------------------------------------------------------------
        try:
            ai_result = self.ai_manager.generate_response(
                system_prompt=system_prompt,
                history=history,
                user_message=message,
            )
        except Exception:
            raise ServiceUnavailableException(
                message="AI assistant is temporarily unavailable. Please try again shortly."
            )

        assistant_message = chat_repository.create_message(
            self.db,
            ChatMessage(
                conversation_id=conversation.id,
                role=ChatRoleEnum.ASSISTANT,
                content=ai_result["text"],
                intent=intent,
                ai_provider=ai_result["provider"],
                tokens_used=ai_result["tokens"],
                response_time_ms=ai_result["response_time_ms"],
            ),
        )

        return {
            "conversation_id": conversation.id,
            "message": assistant_message,
        }

    def get_history(self, user_id: UUID, conversation_id: UUID) -> list[ChatMessage]:
        farmer_profile = farmer_repository.get_by_user_id(self.db, user_id)
        if farmer_profile is None:
            raise NotFoundException(message="Farmer profile not found.")

        conversation = chat_repository.get_conversation_for_farmer(
            self.db, conversation_id, farmer_profile.id
        )
        if conversation is None:
            raise NotFoundException(message="Conversation not found.")

        return chat_repository.get_all_messages(self.db, conversation.id)

    def list_conversations(self, user_id: UUID):
        farmer_profile = farmer_repository.get_by_user_id(self.db, user_id)
        if farmer_profile is None:
            raise NotFoundException(message="Farmer profile not found.")

        return chat_repository.get_conversations_for_farmer(self.db, farmer_profile.id)