"""add otp rate limit table

Revision ID: d4e5f6a7b8c9
Revises: c0c880d704e7
Create Date: 2026-07-25 00:00:00.000000

Adds rate limiting on OTP send requests, keyed by mobile number
(not user_id — at send-otp time for a new registration, no User
row exists yet). Uses the same atomic-upsert-friendly design as
chat_rate_limits / feature_rate_limits: one row per (mobile,
window_start), incremented via INSERT ... ON CONFLICT DO UPDATE
for race safety under concurrent requests.

Module:
Phase 1 → Module 1 → Authentication (Hardening)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, Sequence[str], None] = "c0c880d704e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "otp_rate_limits",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("mobile", sa.String(length=20), nullable=False),
        # Start of the current rate-limit window. A new window is
        # opened (new row) once the previous one expires — this is
        # cheaper than a sliding-window log for OTP-scale traffic.
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), onupdate=sa.text("now()"), nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("mobile", name="uq_otp_rate_limit_mobile"),
    )
    op.create_index("idx_otp_rate_limit_mobile", "otp_rate_limits", ["mobile"])


def downgrade() -> None:
    op.drop_index("idx_otp_rate_limit_mobile", table_name="otp_rate_limits")
    op.drop_table("otp_rate_limits")