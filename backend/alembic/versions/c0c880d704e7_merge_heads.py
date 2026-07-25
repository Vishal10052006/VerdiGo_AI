"""merge heads

Revision ID: c0c880d704e7
Revises: b2c8f4e1a736
Create Date: 2026-07-25 07:42:47.292769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0c880d704e7'
down_revision: Union[str, Sequence[str], None] = 'b2c8f4e1a736'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
