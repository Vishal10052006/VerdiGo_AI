import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class OTP(Base):
    __tablename__ = "otp"

    # =========================
    # Primary Key
    # =========================
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # =========================
    # OTP Information
    # =========================
    mobile = Column(
        String(20),
        nullable=False,
        index=True
    )

    otp = Column(
        String(6),
        nullable=False
    )

    expiry_time = Column(
        DateTime(timezone=True),
        nullable=False
    )

    attempt_count = Column(
        Integer,
        default=0,
        nullable=False
    )

    is_used = Column(
        Boolean,
        default=False,
        nullable=False
    )

    # =========================
    # Timestamp
    # =========================
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )