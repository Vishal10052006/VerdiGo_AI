"""
Weather Provider Request Log Model

Stores every external weather provider request.

Responsibilities:
- Monitor API usage
- Measure response time
- Track fallback usage
- Store provider metadata

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
    Integer,
    String,
    Index,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.weather_provider import WeatherProviderEnum


# ============================================================================
# Weather Provider Request Log Model
# ============================================================================

class WeatherProviderRequestLog(Base):
    """
    Logs external weather provider requests.
    """

    # ------------------------------------------------------------------------
    # Table Configuration
    # ------------------------------------------------------------------------

    __tablename__ = "weather_provider_request_logs"

    __table_args__ = (

        Index(
            "idx_provider_name",
            "provider_name",
        ),

        Index(
            "idx_provider_fetched",
            "fetched_at",
        ),

        Index(
            "idx_provider_status",
            "status_code",
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
    # Provider Information
    # ------------------------------------------------------------------------

    provider_name = Column(
        Enum(WeatherProviderEnum),
        nullable=False,
    )

    provider_version = Column(
        String(30),
        nullable=True,
    )

    # ------------------------------------------------------------------------
    # Request Metrics
    # ------------------------------------------------------------------------

    response_time_ms = Column(
        Integer,
        nullable=False,
    )

    status_code = Column(
        Integer,
        nullable=False,
    )

    fallback_used = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Error Information
    # ------------------------------------------------------------------------

    error_message = Column(
        String(500),
        nullable=True,
    )

    # ------------------------------------------------------------------------
    # Audit Fields
    # ------------------------------------------------------------------------

    fetched_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )