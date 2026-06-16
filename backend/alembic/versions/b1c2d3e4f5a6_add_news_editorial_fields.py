"""add news editorial fields

Revision ID: b1c2d3e4f5a6
Revises: 
Create Date: 2026-06-16
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b1c2d3e4f5a6"
down_revision: Union[str, None] = None
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
    if not column_exists("news", "tags"):
        op.add_column("news", sa.Column("tags", sa.JSON(), nullable=True))
    if not column_exists("news", "categories"):
        op.add_column("news", sa.Column("categories", sa.JSON(), nullable=True))
    if not column_exists("news", "visibility"):
        op.add_column("news", sa.Column("visibility", sa.String(20), server_default="public", nullable=False))
    if not column_exists("news", "scheduled_at"):
        op.add_column("news", sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True))
    if not column_exists("news", "seo_title"):
        op.add_column("news", sa.Column("seo_title", sa.String(255), nullable=True))
    if not column_exists("news", "seo_description"):
        op.add_column("news", sa.Column("seo_description", sa.String(300), nullable=True))
    if not column_exists("news", "seo_keywords"):
        op.add_column("news", sa.Column("seo_keywords", sa.String(500), nullable=True))


def downgrade() -> None:
    columns_to_drop = [
        "seo_keywords",
        "seo_description",
        "seo_title",
        "scheduled_at",
        "visibility",
        "categories",
        "tags",
    ]
    for col_name in columns_to_drop:
        if column_exists("news", col_name):
            op.drop_column("news", col_name)
