"""add author column to news

Revision ID: c1d2e3f4a5b6
Revises: b1c2d3e4f5a6
Create Date: 2026-06-16
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c1d2e3f4a5b6"
down_revision: Union[str, None] = "b1c2d3e4f5a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    result = bind.execute(
        sa.text(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name = :table AND column_name = :col"
        ),
        {"table": table_name, "col": column_name},
    )
    return result.fetchone() is not None


def upgrade() -> None:
    if not column_exists("news", "author"):
        op.add_column("news", sa.Column("author", sa.String(255), nullable=True))


def downgrade() -> None:
    if column_exists("news", "author"):
        op.drop_column("news", "author")
