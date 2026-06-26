"""add credit line detail fields

Revision ID: f2g3h4i5j6k7
Revises: e1f2g3h4i5j6
Create Date: 2026-06-26
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "f2g3h4i5j6k7"
down_revision: Union[str, None] = "e1f2g3h4i5j6"
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
    if not column_exists("credit_lines", "documents"):
        op.add_column("credit_lines", sa.Column("documents", sa.JSON(), nullable=True))
    if not column_exists("credit_lines", "authorization_text"):
        op.add_column("credit_lines", sa.Column("authorization_text", sa.Text(), nullable=True))
    if not column_exists("credit_lines", "external_html"):
        op.add_column("credit_lines", sa.Column("external_html", sa.Text(), nullable=True))


def downgrade() -> None:
    if column_exists("credit_lines", "external_html"):
        op.drop_column("credit_lines", "external_html")
    if column_exists("credit_lines", "authorization_text"):
        op.drop_column("credit_lines", "authorization_text")
    if column_exists("credit_lines", "documents"):
        op.drop_column("credit_lines", "documents")
