"""add crop recommendation tables

Revision ID: b7f3e9a2c481
Revises: a1b2c3d4e5f6
Create Date: 2026-07-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "b7f3e9a2c481"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ------------------------------------------------------------------------
    # Create enum types explicitly, ONCE. Every later reference to these
    # types inside Column()/ARRAY() must pass create_type=False, otherwise
    # SQLAlchemy's table-creation DDL event tries to CREATE TYPE again and
    # collides with what we just created here.
    # ------------------------------------------------------------------------

    season_enum = postgresql.ENUM(
        "KHARIF", "RABI", "ZAID",
        name="seasonenum",
    )
    season_enum.create(op.get_bind(), checkfirst=True)

    water_enum = postgresql.ENUM(
        "LOW", "MEDIUM", "HIGH",
        name="waterrequirementenum",
    )
    water_enum.create(op.get_bind(), checkfirst=True)

    # Non-creating references for use inside table columns below.
    season_enum_ref = postgresql.ENUM(
        "KHARIF", "RABI", "ZAID",
        name="seasonenum",
        create_type=False,
    )
    water_enum_ref = postgresql.ENUM(
        "LOW", "MEDIUM", "HIGH",
        name="waterrequirementenum",
        create_type=False,
    )

    # ------------------------------------------------------------------------
    # Crops (master data)
    # ------------------------------------------------------------------------

    op.create_table(
        "crops",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column(
            "suitable_soil_types",
            postgresql.ARRAY(
                postgresql.ENUM(
                    "CLAY", "SANDY", "LOAMY", "SILTY", "BLACK", "RED",
                    "LATERITE", "ALLUVIAL", "MOUNTAIN", "UNKNOWN",
                    name="soiltypeenum",
                    create_type=False,
                )
            ),
            nullable=False,
        ),
        sa.Column(
            "suitable_seasons",
            postgresql.ARRAY(season_enum_ref),
            nullable=False,
        ),
        sa.Column(
            "suitable_states",
            postgresql.ARRAY(sa.String(length=100)),
            nullable=True,
        ),
        sa.Column("water_requirement", water_enum_ref, nullable=False),
        sa.Column("ideal_temp_min", sa.Float(), nullable=True),
        sa.Column("ideal_temp_max", sa.Float(), nullable=True),
        sa.Column("growth_duration_days", sa.Integer(), nullable=False),
        sa.Column("expected_yield_per_acre", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("idx_crops_active", "crops", ["is_active"], unique=False)

    # ------------------------------------------------------------------------
    # Crop Recommendations (run history)
    # ------------------------------------------------------------------------

    op.create_table(
        "crop_recommendations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farm_id", sa.UUID(), nullable=False),
        sa.Column("season", season_enum_ref, nullable=False),
        sa.Column("source", sa.String(length=20), nullable=False, server_default="rule_based"),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["farm_id"], ["farms.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_crop_reco_farm", "crop_recommendations", ["farm_id"], unique=False)

    # ------------------------------------------------------------------------
    # Crop Recommendation Items
    # ------------------------------------------------------------------------

    op.create_table(
        "crop_recommendation_items",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("recommendation_id", sa.UUID(), nullable=False),
        sa.Column("crop_id", sa.UUID(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("reasoning", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["recommendation_id"], ["crop_recommendations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["crop_id"], ["crops.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_crop_reco_items_reco", "crop_recommendation_items", ["recommendation_id"], unique=False)

def downgrade() -> None:
    op.drop_index("idx_crop_reco_items_reco", table_name="crop_recommendation_items")
    op.drop_table("crop_recommendation_items")

    op.drop_index("idx_crop_reco_farm", table_name="crop_recommendations")
    op.drop_table("crop_recommendations")

    op.drop_index("idx_crops_active", table_name="crops")
    op.drop_table("crops")

    postgresql.ENUM(name="waterrequirementenum").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="seasonenum").drop(op.get_bind(), checkfirst=True)