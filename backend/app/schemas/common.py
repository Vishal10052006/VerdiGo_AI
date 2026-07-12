"""
Common Schemas

Shared response schemas used throughout the VerdiGO backend.

Responsibilities:
- Standard success response
- Standard error response
- Standard paginated response

Module:
Shared

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from typing import Any
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

# ============================================================================
# Generic Type
# ============================================================================

T = TypeVar("T")

# ============================================================================
# Success Response
# ============================================================================


class SuccessResponse(GenericModel, Generic[T]):
    """
    Standard success response.

    Used by all successful API endpoints.
    """

    success: bool = True

    message: str

    data: T


# ============================================================================
# Error Response
# ============================================================================


class ErrorResponse(BaseModel):
    """
    Standard error response.

    Used by all failed API endpoints.
    """

    success: bool = False

    message: str

    error_code: str | None = None

    details: Any | None = None


# ============================================================================
# Paginated Response
# ============================================================================


class PaginatedResponse(GenericModel, Generic[T]):
    """
    Standard paginated response.

    Used for list APIs with pagination.
    """

    success: bool = True

    message: str

    data: list[T]

    total: int

    page: int

    page_size: int