# backend/app/scripts/seed_admin.py
"""
Seed First Admin

Usage:
    python -m app.scripts.seed_admin --email you@verdigo.ai --password "StrongPass123!" --name "Vishal Raj"

Module: Phase 1 → Module 10 → Admin Panel
"""

import argparse

from app.database.database import SessionLocal
from app.models.admin_user import AdminUser
from app.enums.admin import AdminRoleEnum
from app.services.admin_auth_service import hash_password
from app.repositories import admin_repository


def seed_admin(email: str, password: str, full_name: str) -> None:
    db = SessionLocal()
    try:
        existing = admin_repository.get_by_email(db=db, email=email.lower())
        if existing:
            print(f"⚠️  Admin with email {email} already exists.")
            return

        admin = AdminUser(
            email=email.lower(),
            password_hash=hash_password(password),
            full_name=full_name,
            role=AdminRoleEnum.SUPER_ADMIN,
            is_active=True,
        )
        admin_repository.create(db=db, admin=admin)
        print(f"✅ Super admin created: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    seed_admin(args.email, args.password, args.name)