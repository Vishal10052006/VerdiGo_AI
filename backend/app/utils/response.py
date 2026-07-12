"""
Response Utilities

Provides standardized API response builders used across
the VerdiGO backend.

Responsibilities:
- Success response
- Error response
- Keep routes clean

Module:
Shared Utility

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from typing import Any, Type

from pydantic import BaseModel

from app.schemas.common import (
    SuccessResponse,
    ErrorResponse,
)

# ============================================================================
# Success Response
# ============================================================================

def success_response(
    schema: Type[BaseModel],
    data: dict | BaseModel,
    message: str,
) -> SuccessResponse:
    """
    Build a standardized successful API response.
    """

    if isinstance(data, BaseModel):
        response_data = data
    else:
        response_data = schema(**data)

    return SuccessResponse(
        success=True,
        message=message,
        data=response_data,
    )


# ============================================================================
# Error Response
# ============================================================================

def error_response(
    message: str,
    data: Any = None,
) -> ErrorResponse:
    """
    Build a standardized error response.
    """

    return ErrorResponse(
        success=False,
        message=message,
    )