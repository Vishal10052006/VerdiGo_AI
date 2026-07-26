"""add google oauth support — nullable mobile, google_id column

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-07-26 00:00:00.000000

Makes `mobile` nullable since Google-signup users won't have one at
signup time (they can add it later via a "complete your profile"
prompt — see profile_service.py). Adds `google_id` as the stable
Google account identifier (NOT email — emails can theoretically be
reused/changed on Google's side over long timescales, google's `sub`
claim is the documented stable identifier).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e5f6a7b8c9d0"
down_revision: Union[str, Sequence[str], None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "mobile", existing_type=sa.String(length=20), nullable=True)

    op.drop_index("ix_users_mobile", table_name="users")
    op.create_index(
        "ix_users_mobile", "users", ["mobile"], unique=True,
        postgresql_where=sa.text("mobile IS NOT NULL"),
    )

    op.add_column(
        "users",
        sa.Column("google_id", sa.String(length=255), nullable=True),
    )
    op.create_index(
        "ix_users_google_id", "users", ["google_id"], unique=True,
        postgresql_where=sa.text("google_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_users_google_id", table_name="users")
    op.drop_column("users", "google_id")

    op.drop_index("ix_users_mobile", table_name="users")
    op.create_index("ix_users_mobile", "users", ["mobile"], unique=True)
    op.alter_column("users", "mobile", existing_type=sa.String(length=20), nullable=False)
