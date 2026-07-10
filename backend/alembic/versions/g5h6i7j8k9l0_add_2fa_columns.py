"""add 2fa columns to users

Revision ID: g5h6i7j8k9l0
Revises: f2g3h4i5j6k7
Create Date: 2026-07-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "g5h6i7j8k9l0"
down_revision: Union[str, None] = "f2g3h4i5j6k7"
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
    if not column_exists("users", "totp_secret"):
        op.add_column("users", sa.Column("totp_secret", sa.String(32), nullable=True))
    if not column_exists("users", "two_factor_enabled"):
        op.add_column("users", sa.Column("two_factor_enabled", sa.Boolean(), server_default="false", nullable=False))


def downgrade() -> None:
    if column_exists("users", "two_factor_enabled"):
        op.drop_column("users", "two_factor_enabled")
    if column_exists("users", "totp_secret"):
        op.drop_column("users", "totp_secret")
