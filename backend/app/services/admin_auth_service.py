# backend/app/services/admin_auth_service.py
"""
Admin Auth Service

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.repositories import admin_repository
from app.services.jwt_service import create_access_token
from app.core.exceptions import UnauthorizedException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def login_admin(db: Session, email: str, password: str) -> dict:
    admin = admin_repository.get_by_email(db=db, email=email.lower().strip())

    if admin is None or not verify_password(password, admin.password_hash):
        # Same message for both cases — don't leak which part failed.
        raise UnauthorizedException(message="Invalid email or password.")

    if not admin.is_active:
        raise UnauthorizedException(message="This admin account has been deactivated.")

    # Admin tokens carry a distinct "sub" namespace via jti/type reuse of
    # jwt_service — token "type" stays "access" (verified generically),
    # but we tag the subject so get_current_admin can resolve it against
    # AdminUser, not User.
    access_token, _jti, _exp = create_access_token(f"admin:{admin.id}")

    admin_repository.update_last_login(db=db, admin=admin)

    return {"access_token": access_token, "admin": admin}