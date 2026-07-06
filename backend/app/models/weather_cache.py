"""
Weather Cache Model

Stores cached weather responses to reduce external API calls
and improve application performance.

Responsibilities:
- Cache current weather
- Cache forecast weather
- Track provider used
- Store cache expiry

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    JSON,
    Index,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.weather_provider import WeatherProviderEnum
from app.enums.weather_type import WeatherTypeEnum


# ============================================================================
# Weather Cache Model
# ============================================================================

class WeatherCache(Base):
    """
    Stores cached weather responses for farms.
    """

    # ------------------------------------------------------------------------
    # Table Configuration
    # ------------------------------------------------------------------------

    __tablename__ = "weather_cache"

    __table_args__ = (

        # Lookup weather by farm
        Index(
            "idx_weather_cache_farm",
            "farm_id",
        ),

        # Lookup by expiry
        Index(
            "idx_weather_cache_expiry",
            "expires_at",
        ),

        # Farm + Weather Type
        Index(
            "idx_weather_cache_farm_type",
            "farm_id",
            "weather_type",
        ),

    )

    # ------------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------------

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ------------------------------------------------------------------------
    # Farm Reference
    # ------------------------------------------------------------------------

    farm_id = Column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Weather Metadata
    # ------------------------------------------------------------------------

    weather_type = Column(
        Enum(WeatherTypeEnum),
        nullable=False,
    )

    provider_name = Column(
        Enum(WeatherProviderEnum),
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Location
    # ------------------------------------------------------------------------

    latitude = Column(
        Float,
        nullable=False,
    )

    longitude = Column(
        Float,
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Cached Response
    # ------------------------------------------------------------------------

    weather_data = Column(
        JSON,
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Cache Information
    # ------------------------------------------------------------------------

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Audit Fields
    # ------------------------------------------------------------------------

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------------

    farm = relationship(
        "Farm",
        back_populates="weather_cache",
    )