import argparse
import getpass

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
    # FIX: password no longer accepted as a CLI arg (--password), which
    # would appear in shell history and `ps`/process listings. Now
    # prompted interactively via getpass (input not echoed to terminal,
    # not stored in shell history).
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    password = getpass.getpass("Admin password: ")
    password_confirm = getpass.getpass("Confirm password: ")

    if password != password_confirm:
        print("❌ Passwords do not match.")
        raise SystemExit(1)

    seed_admin(args.email, password, args.name)