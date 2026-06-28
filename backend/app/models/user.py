import uuid
from sqlalchemy import (
    Column,
    Boolean,
    DateTime,
    String
)

from sqlalchemy import (
    Boolean,
    DateTime,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    # =========================
    # Primary Key
    # =========================
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # =========================
    # Authentication
    # =========================
    mobile = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(255),
        unique=True,
        nullable=True
    )

    auth_provider = Column(
        String(20),
        default="otp",
        nullable=False
    )

    # =========================
    # Profile
    # =========================
    full_name = Column(
        String(255),
        nullable=True
    )

    profile_image = Column(
        String(500),
        nullable=True
    )

    language = Column(
        String(20),
        default="hi",
        nullable=False
    )

    role = Column(
        String(20),
        default="farmer",
        nullable=False
    )

    # =========================
    # Status
    # =========================
    is_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    # =========================
    # Timestamps
    # =========================
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # =========================
    # Relationships
    # =========================

    # One User -> One Farmer Profile
    farmer_profile = relationship(
        "FarmerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )