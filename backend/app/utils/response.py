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
    data: dict | BaseModel | list,
    message: str,
) -> SuccessResponse:
    """
    Build a standardized successful API response.

    Accepts:
    - a BaseModel instance (returned as-is)
    - a list of BaseModel instances (returned as-is, e.g. list endpoints
      like GET /v1/chat/conversations — already validated by the caller)
    - a dict (unpacked into `schema(**data)`)
    """

    if isinstance(data, BaseModel):
        response_data = data
    elif isinstance(data, list):
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