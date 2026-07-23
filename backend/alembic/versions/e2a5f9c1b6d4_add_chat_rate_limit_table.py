# backend/alembic/versions/e2a5f9c1b6d4_add_chat_rate_limit_table.py
"""add chat rate limit table

Revision ID: e2a5f9c1b6d4
Revises: c9d4f1a7e832
Create Date: 2026-07-22 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e2a5f9c1b6d4"
down_revision: Union[str, Sequence[str], None] = "c9d4f1a7e832"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chat_rate_limits",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farmer_profile_id", sa.UUID(), nullable=False),
        sa.Column("usage_date", sa.Date(), nullable=False),
        sa.Column("message_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["farmer_profile_id"], ["farmer_profiles.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "farmer_profile_id", "usage_date", name="uq_chat_rate_limit_farmer_date"
        ),
    )
    op.create_index(
        "idx_chat_rate_limit_farmer_date",
        "chat_rate_limits",
        ["farmer_profile_id", "usage_date"],
    )


def downgrade() -> None:
    op.drop_index("idx_chat_rate_limit_farmer_date", table_name="chat_rate_limits")
    op.drop_table("chat_rate_limits")