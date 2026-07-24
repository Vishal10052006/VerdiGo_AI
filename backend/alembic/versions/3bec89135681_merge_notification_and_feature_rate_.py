"""merge notification and feature rate limit heads

Revision ID: 3bec89135681
Revises: a3f7c8e2b1d9, a3f7e1b2c9d5
Create Date: 2026-07-24 13:15:04.051371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bec89135681'
down_revision: Union[str, Sequence[str], None] = ('a3f7c8e2b1d9', 'a3f7e1b2c9d5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
