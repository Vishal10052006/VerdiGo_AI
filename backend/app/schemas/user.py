"""
User Schemas

This module defines all Pydantic schemas used for User APIs.

Responsibilities:
- Validate user request data.
- Serialize user responses.
- Provide internal and public user response models.

Module:
Phase 1 → Module 3 → Farmer Profile

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)

# ============================================================================
# User Create Request
# ============================================================================

class UserCreate(BaseModel):
    """
    Request schema for creating a user.
    """

    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    login_type: str


# ============================================================================
# User Internal Response
# ============================================================================

class UserResponse(BaseModel):
    """
    Internal response schema.

    Used by backend services, authentication,
    and internal APIs.
    """

    id: UUID

    mobile: str
    email: Optional[str] = None

    profile_image_url: Optional[str] = None

    language: str

    role: str

    is_verified: bool

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================================
# User Public Response
# ============================================================================

class UserPublicResponse(BaseModel):
    """
    Public response schema.

    Used by profile APIs exposed to the
    farmer mobile application.
    """

    id: UUID

    mobile: str

    email: Optional[str] = None

    profile_image_url: Optional[str] = None

    language: str

    model_config = ConfigDict(
        from_attributes=True
    )