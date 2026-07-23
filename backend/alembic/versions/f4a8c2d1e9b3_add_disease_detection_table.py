"""add disease_detections table

Revision ID: f4a8c2d1e9b3
Revises: e2a5f9c1b6d4
Create Date: 2026-07-23 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f4a8c2d1e9b3"
down_revision: Union[str, Sequence[str], None] = "e2a5f9c1b6d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "disease_detections",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farm_id", sa.UUID(), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=False),
        sa.Column("crop_type", sa.String(length=100), nullable=True),
        sa.Column("is_healthy", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("disease_name", sa.String(length=150), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0"),
        sa.Column(
            "severity",
            sa.Enum("NONE", "LOW", "MODERATE", "HIGH", "CRITICAL", name="diseaseseverityenum"),
            nullable=False,
            server_default="NONE",
        ),
        sa.Column("treatment", sa.JSON(), nullable=False),
        sa.Column("prevention_tips", sa.JSON(), nullable=False),
        sa.Column("ai_provider", sa.String(length=20), nullable=False, server_default="gemini"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["farm_id"], ["farms.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_disease_detection_farm", "disease_detections", ["farm_id"])
    op.create_index("idx_disease_detection_created", "disease_detections", ["created_at"])
    op.create_index("idx_disease_detection_severity", "disease_detections", ["severity"])


def downgrade() -> None:
    op.drop_index("idx_disease_detection_severity", table_name="disease_detections")
    op.drop_index("idx_disease_detection_created", table_name="disease_detections")
    op.drop_index("idx_disease_detection_farm", table_name="disease_detections")
    op.drop_table("disease_detections")
    sa.Enum(name="diseaseseverityenum").drop(op.get_bind(), checkfirst=True)