"""
Admin User Model

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.admin import AdminRoleEnum


class AdminUser(Base):
    __tablename__ = "admin_users"

    __table_args__ = (Index("idx_admin_users_email", "email"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)

    role = Column(Enum(AdminRoleEnum), nullable=False, default=AdminRoleEnum.ADMIN)

    is_active = Column(Boolean, default=True, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,
    )