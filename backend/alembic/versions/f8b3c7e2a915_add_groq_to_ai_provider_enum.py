"""add groq to aiproviderenum

Revision ID: f8b3c7e2a915
Revises: f4a8c2d1e9b3
Create Date: 2026-07-24 00:00:00.000000
"""
from alembic import op

revision = "f8b3c7e2a915"
down_revision = "f4a8c2d1e9b3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE aiproviderenum ADD VALUE IF NOT EXISTS 'GROQ'")


def downgrade() -> None:
    # Postgres doesn't support removing enum values directly.
    # Safe no-op — leaving 'GROQ' in the type causes no harm on downgrade.
    pass