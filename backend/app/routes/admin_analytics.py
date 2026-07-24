# backend/app/routes/admin_analytics.py
"""
Admin Analytics Routes

Module: Phase 1 → Module 10 → Admin Panel
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.admin_auth import get_current_admin
from app.models.admin_user import AdminUser

from app.schemas.common import SuccessResponse
from app.schemas.admin import AnalyticsOverviewSchema, GrowthAnalyticsSchema
from app.services import admin_analytics_service
from app.utils.response import success_response

router = APIRouter(prefix="/admin/analytics", tags=["Admin Analytics"])


@router.get("/overview", response_model=SuccessResponse[AnalyticsOverviewSchema])
def get_overview(
    db: Session = Depends(get_db),
    _admin: AdminUser = Depends(get_current_admin),
):
    data = admin_analytics_service.get_overview(db)

    return success_response(
        schema=AnalyticsOverviewSchema,
        data=data,
        message="Analytics overview retrieved successfully.",
    )


@router.get("/growth", response_model=SuccessResponse[GrowthAnalyticsSchema])
def get_growth(
    days: int = Query(30, ge=1, le=180),
    db: Session = Depends(get_db),
    _admin: AdminUser = Depends(get_current_admin),
):
    data = admin_analytics_service.get_growth(db, days=days)

    return success_response(
        schema=GrowthAnalyticsSchema,
        data=data,
        message="Growth analytics retrieved successfully.",
    )