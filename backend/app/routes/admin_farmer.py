# backend/app/routes/admin_farmer.py
"""
Admin Farmer Management Routes

Module: Phase 1 → Module 10 → Admin Panel
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.admin_auth import get_current_admin
from app.models.admin_user import AdminUser

from app.schemas.common import SuccessResponse
from app.schemas.admin import (
    FarmerListResponseSchema,
    FarmerDetailSchema,
    UpdateFarmerStatusRequest,
)
from app.services import admin_farmer_service
from app.utils.response import success_response

router = APIRouter(prefix="/admin/farmers", tags=["Admin Farmer Management"])


@router.get("", response_model=SuccessResponse[FarmerListResponseSchema])
def list_farmers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    state: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    _admin: AdminUser = Depends(get_current_admin),
):
    result = admin_farmer_service.list_farmers(
        db=db, page=page, page_size=page_size, search=search, state=state, is_active=is_active,
    )

    return success_response(
        schema=FarmerListResponseSchema,
        data=result,
        message="Farmers retrieved successfully.",
    )


@router.get("/{user_id}", response_model=SuccessResponse[FarmerDetailSchema])
def get_farmer(
    user_id: UUID,
    db: Session = Depends(get_db),
    _admin: AdminUser = Depends(get_current_admin),
):
    detail = admin_farmer_service.get_farmer_detail(db=db, user_id=user_id)

    return success_response(
        schema=FarmerDetailSchema,
        data=FarmerDetailSchema.model_validate(detail),
        message="Farmer details retrieved successfully.",
    )


@router.patch("/{user_id}/status", response_model=SuccessResponse[FarmerDetailSchema])
def update_farmer_status(
    user_id: UUID,
    request: UpdateFarmerStatusRequest,
    db: Session = Depends(get_db),
    _admin: AdminUser = Depends(get_current_admin),
):
    detail = admin_farmer_service.set_farmer_status(
        db=db, user_id=user_id, is_active=request.is_active,
    )

    return success_response(
        schema=FarmerDetailSchema,
        data=FarmerDetailSchema.model_validate(detail),
        message="Farmer status updated successfully.",
    )