# backend/app/routes/admin_auth.py
"""
Admin Auth Routes

Module: Phase 1 → Module 10 → Admin Panel
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.admin import AdminLoginRequest, AdminLoginResponse, AdminResponse
from app.services.admin_auth_service import login_admin
from app.dependencies.admin_auth import get_current_admin
from app.models.admin_user import AdminUser

router = APIRouter(prefix="/admin/auth", tags=["Admin Auth"])


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    result = login_admin(db=db, email=request.email, password=request.password)

    return AdminLoginResponse(
        access_token=result["access_token"],
        admin=AdminResponse.model_validate(result["admin"]),
    )


@router.get("/me", response_model=AdminResponse)
def get_me(admin: AdminUser = Depends(get_current_admin)):
    return admin