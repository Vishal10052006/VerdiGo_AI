from pydantic import BaseModel, EmailStr
from typing import Optional

from uuid import UUID

from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    login_type: str


class UserResponse(BaseModel):
    id: UUID
    mobile: str
    email: str | None
    full_name: str | None
    profile_image: str | None
    language: str
    role: str
    is_verified: bool
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )