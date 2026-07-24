"""add feature_rate_limits table

Revision ID: a3f7e1b2c9d5
Revises: f4a8c2d1e9b3
Create Date: 2026-07-24 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a3f7e1b2c9d5"
down_revision: Union[str, Sequence[str], None] = "f8b3c7e2a915"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "feature_rate_limits",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farmer_profile_id", sa.UUID(), nullable=False),
        sa.Column("feature", sa.String(length=50), nullable=False),
        sa.Column("usage_date", sa.Date(), nullable=False),
        sa.Column("usage_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), onupdate=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(["farmer_profile_id"], ["farmer_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "farmer_profile_id", "feature", "usage_date",
            name="uq_feature_rate_limit_farmer_feature_date",
        ),
    )
    op.create_index(
        "idx_feature_rate_limit_lookup",
        "feature_rate_limits",
        ["farmer_profile_id", "feature", "usage_date"],
    )


def downgrade() -> None:
    op.drop_index("idx_feature_rate_limit_lookup", table_name="feature_rate_limits")
    op.drop_table("feature_rate_limits")