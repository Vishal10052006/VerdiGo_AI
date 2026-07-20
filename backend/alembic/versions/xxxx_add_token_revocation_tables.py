"""add refresh_tokens and token_blacklist tables for real logout

Revision ID: a1b2c3d4e5f6
Revises: dc7dcb4de359
Create Date: 2026-07-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "dc7dcb4de359"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("jti", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("jti"),
    )
    op.create_index("idx_refresh_token_jti", "refresh_tokens", ["jti"])
    op.create_index("idx_refresh_token_user", "refresh_tokens", ["user_id"])

    op.create_table(
        "token_blacklist",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("jti", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("jti"),
    )
    op.create_index("idx_blacklist_jti", "token_blacklist", ["jti"])
    op.create_index("idx_blacklist_expiry", "token_blacklist", ["expires_at"])


def downgrade() -> None:
    op.drop_index("idx_blacklist_expiry", table_name="token_blacklist")
    op.drop_index("idx_blacklist_jti", table_name="token_blacklist")
    op.drop_table("token_blacklist")

    op.drop_index("idx_refresh_token_user", table_name="refresh_tokens")
    op.drop_index("idx_refresh_token_jti", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")