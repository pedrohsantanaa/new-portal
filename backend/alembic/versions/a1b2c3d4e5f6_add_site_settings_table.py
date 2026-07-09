"""add site_settings table

Revision ID: a1b2c3d4e5f6
Revises: 0997102c8102
Create Date: 2026-07-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "0997102c8102"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    result = bind.execute(
        sa.text(
            "SELECT 1 FROM information_schema.tables "
            "WHERE table_name = :table"
        ),
        {"table": table_name},
    )
    return result.fetchone() is not None


def upgrade() -> None:
    if not table_exists("site_settings"):
        op.create_table(
            "site_settings",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("key", sa.String(100), unique=True, nullable=False, index=True),
            sa.Column("value", sa.Boolean(), nullable=False, server_default="true"),
            sa.Column("label", sa.String(200), nullable=False),
            sa.Column("group", sa.String(50), nullable=False),
            sa.Column("order", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

        settings_table = sa.table(
            "site_settings",
            sa.column("key", sa.String),
            sa.column("value", sa.Boolean),
            sa.column("label", sa.String),
            sa.column("group", sa.String),
            sa.column("order", sa.Integer),
            sa.column("created_at", sa.DateTime),
            sa.column("updated_at", sa.DateTime),
        )
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        op.bulk_insert(
            settings_table,
            [
                {"key": "home_hero", "value": True, "label": "Banner Principal (Hero)", "group": "home", "order": 1, "created_at": now, "updated_at": now},
                {"key": "home_creditos", "value": True, "label": "Seção de Créditos", "group": "home", "order": 2, "created_at": now, "updated_at": now},
                {"key": "home_noticias", "value": True, "label": "Seção de Notícias", "group": "home", "order": 3, "created_at": now, "updated_at": now},
                {"key": "home_parceiros", "value": True, "label": "Seção de Parceiros", "group": "home", "order": 4, "created_at": now, "updated_at": now},
                {"key": "page_noticias", "value": True, "label": "Página de Notícias", "group": "pages", "order": 1, "created_at": now, "updated_at": now},
                {"key": "page_creditos", "value": True, "label": "Página de Linhas de Crédito", "group": "pages", "order": 2, "created_at": now, "updated_at": now},
                {"key": "page_acesso", "value": True, "label": "Página de Acesso à Informação", "group": "pages", "order": 3, "created_at": now, "updated_at": now},
                {"key": "page_institucional", "value": True, "label": "Página Institucional", "group": "pages", "order": 4, "created_at": now, "updated_at": now},
                {"key": "nav_creditos", "value": True, "label": "Link \"Linhas de Crédito\" no Menu", "group": "nav", "order": 1, "created_at": now, "updated_at": now},
                {"key": "nav_noticias", "value": True, "label": "Link \"Notícias\" no Menu", "group": "nav", "order": 2, "created_at": now, "updated_at": now},
                {"key": "nav_acesso", "value": True, "label": "Link \"Acesso à Informação\" no Menu", "group": "nav", "order": 3, "created_at": now, "updated_at": now},
                {"key": "nav_institucional", "value": True, "label": "Link \"Institucional\" no Menu", "group": "nav", "order": 4, "created_at": now, "updated_at": now},
            ],
        )


def downgrade() -> None:
    if table_exists("site_settings"):
        op.drop_table("site_settings")
