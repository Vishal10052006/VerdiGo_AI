# backend/app/dependencies/admin_auth.py
"""
Admin Auth Dependency

Mirrors dependencies/auth.py but resolves against AdminUser
instead of User, using the "admin:<uuid>" subject convention
set in admin_auth_service.login_admin.

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.database.database import get_db
from app.models.admin_user import AdminUser
from app.repositories import admin_repository
from app.services.jwt_service import verify_token
from app.enums.admin import AdminRoleEnum

bearer_scheme = HTTPBearer(auto_error=True)


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AdminUser:
    payload = verify_token(token=credentials.credentials, token_type="access")

    if payload is None:
        raise UnauthorizedException()

    subject = payload.get("sub", "")

    if not subject.startswith("admin:"):
        # A valid farmer token used against an admin route.
        raise UnauthorizedException(message="Admin access required.")

    admin_id = subject.removeprefix("admin:")
    admin = admin_repository.get_by_id(db=db, admin_id=admin_id)

    if admin is None or not admin.is_active:
        raise UnauthorizedException()

    return admin


def get_current_super_admin(
    admin: AdminUser = Depends(get_current_admin),
) -> AdminUser:
    if admin.role != AdminRoleEnum.SUPER_ADMIN:
        raise ForbiddenException(message="Super admin access required.")
    return admin