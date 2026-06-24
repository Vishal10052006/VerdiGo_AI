from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class UserCreate(BaseModel):
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    login_type: str


class UserResponse(BaseModel):
    id: UUID
    mobile: Optional[str]
    email: Optional[str]
    login_type: str

    class Config:
        from_attributes = True