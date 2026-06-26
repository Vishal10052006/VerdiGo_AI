from typing import Any

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Any | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str


class PaginatedResponse(BaseModel):
    success: bool = True
    message: str
    data: list[Any]
    total: int
    page: int
    page_size: int