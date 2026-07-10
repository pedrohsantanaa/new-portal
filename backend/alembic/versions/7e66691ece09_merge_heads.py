"""Merge heads

Revision ID: 7e66691ece09
Revises: c3d4e5f6a7b8, g5h6i7j8k9l0
Create Date: 2026-07-10 16:48:36.532623
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7e66691ece09'
down_revision: Union[str, None] = ('c3d4e5f6a7b8', 'g5h6i7j8k9l0')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
