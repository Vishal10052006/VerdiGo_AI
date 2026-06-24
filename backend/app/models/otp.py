from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database.base import Base


class OTP(Base):
    __tablename__ = "otp_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    mobile = Column(String, nullable=False)

    otp = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)