# backend/app/services/admin_auth_service.py
"""
Admin Auth Service

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

import bcrypt
from sqlalchemy.orm import Session

from app.repositories import admin_repository
from app.services.jwt_service import create_access_token
from app.core.exceptions import UnauthorizedException

_BCRYPT_MAX_BYTES = 72  # bcrypt's hard limit — enforce explicitly, don't rely on a library to catch it


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > _BCRYPT_MAX_BYTES:
        raise ValueError(f"Password must be at most {_BCRYPT_MAX_BYTES} bytes.")

    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        # Malformed hash in DB — treat as a failed verification, not a crash.
        return False


def login_admin(db: Session, email: str, password: str) -> dict:
    admin = admin_repository.get_by_email(db=db, email=email.lower().strip())

    if admin is None or not verify_password(password, admin.password_hash):
        raise UnauthorizedException(message="Invalid email or password.")

    if not admin.is_active:
        raise UnauthorizedException(message="This admin account has been deactivated.")

    access_token, _jti, _exp = create_access_token(f"admin:{admin.id}")

    admin_repository.update_last_login(db=db, admin=admin)

    return {"access_token": access_token, "admin": admin}