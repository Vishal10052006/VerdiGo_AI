"""
refactor_user_profile_fields

Revision ID: 235802a55798
Revises: cd83f6534134
Create Date: 2026-06-29 16:24:12.660872
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# ============================================================================
# Alembic Revision Identifiers
# ============================================================================

revision: str = "235802a55798"
down_revision: Union[str, Sequence[str], None] = "cd83f6534134"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ============================================================================
# Upgrade Migration
# ============================================================================

def upgrade() -> None:
    """
    Upgrade database schema.

    Changes:
    - Remove duplicated `full_name` from users table.
    - Replace `profile_image` with `profile_image_url`.
    """

    # ------------------------------------------------------------------------
    # Add new profile image URL column
    # ------------------------------------------------------------------------
    op.add_column(
        "users",
        sa.Column(
            "profile_image_url",
            sa.String(length=500),
            nullable=True,
            comment="Relative or absolute URL of the user's profile image.",
        ),
    )

    # ------------------------------------------------------------------------
    # Remove duplicated user name
    # (FarmerProfile is now the single source of truth)
    # ------------------------------------------------------------------------
    op.drop_column("users", "full_name")

    # ------------------------------------------------------------------------
    # Remove old profile image column
    # Safe because the MVP database contains no image data.
    # ------------------------------------------------------------------------
    op.drop_column("users", "profile_image")


# ============================================================================
# Downgrade Migration
# ============================================================================

def downgrade() -> None:
    """
    Revert database schema.
    """

    # ------------------------------------------------------------------------
    # Restore old profile image column
    # ------------------------------------------------------------------------
    op.add_column(
        "users",
        sa.Column(
            "profile_image",
            sa.String(length=500),
            nullable=True,
        ),
    )

    # ------------------------------------------------------------------------
    # Restore full_name column
    # ------------------------------------------------------------------------
    op.add_column(
        "users",
        sa.Column(
            "full_name",
            sa.String(length=255),
            nullable=True,
        ),
    )

    # ------------------------------------------------------------------------
    # Remove profile_image_url column
    # ------------------------------------------------------------------------
    op.drop_column("users", "profile_image_url")