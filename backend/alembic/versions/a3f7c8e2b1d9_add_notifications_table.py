"""add notifications table

Revision ID: a3f7c8e2b1d9
Revises: f4a8c2d1e9b3
Create Date: 2026-07-24 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a3f7c8e2b1d9"
down_revision: Union[str, Sequence[str], None] = "f4a8c2d1e9b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farmer_profile_id", sa.UUID(), nullable=False),
        sa.Column(
            "type",
            sa.Enum("WEATHER", "DISEASE", "CROP", "SYSTEM", "GENERAL", name="notificationtypeenum"),
            nullable=False,
        ),
        sa.Column(
            "severity",
            sa.Enum("INFO", "LOW", "MODERATE", "HIGH", "CRITICAL", name="notificationseverityenum"),
            nullable=False,
            server_default="INFO",
        ),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("related_entity_id", sa.UUID(), nullable=True),
        sa.Column("related_entity_type", sa.String(length=50), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["farmer_profile_id"], ["farmer_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_notification_farmer", "notifications", ["farmer_profile_id"])
    op.create_index("idx_notification_farmer_read", "notifications", ["farmer_profile_id", "is_read"])
    op.create_index("idx_notification_created", "notifications", ["created_at"])


def downgrade() -> None:
    op.drop_index("idx_notification_created", table_name="notifications")
    op.drop_index("idx_notification_farmer_read", table_name="notifications")
    op.drop_index("idx_notification_farmer", table_name="notifications")
    op.drop_table("notifications")
    sa.Enum(name="notificationseverityenum").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="notificationtypeenum").drop(op.get_bind(), checkfirst=True)