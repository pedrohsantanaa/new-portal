"""add categories, permissions and user permissions

Revision ID: d4e5f6a7b8c9
Revises: c1d2e3f4a5b6
Create Date: 2026-06-22
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, None] = "c1d2e3f4a5b6"
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
    # Tabela categories
    if not table_exists("categories"):
        op.create_table(
            "categories",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(100), unique=True, nullable=False),
            sa.Column("slug", sa.String(100), unique=True, nullable=False, index=True),
            sa.Column("description", sa.String(255), nullable=True),
            sa.Column("active", sa.Boolean(), server_default="true", nullable=False),
            sa.Column("order", sa.Integer(), server_default="0", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

        # Categorias padrão
        categories_table = sa.table(
            "categories",
            sa.column("name", sa.String),
            sa.column("slug", sa.String),
            sa.column("order", sa.Integer),
            sa.column("active", sa.Boolean),
            sa.column("created_at", sa.DateTime),
            sa.column("updated_at", sa.DateTime),
        )
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        op.bulk_insert(
            categories_table,
            [
                {"name": "Crédito", "slug": "credito", "order": 1, "active": True, "created_at": now, "updated_at": now},
                {"name": "Programa", "slug": "programa", "order": 2, "active": True, "created_at": now, "updated_at": now},
                {"name": "Evento", "slug": "evento", "order": 3, "active": True, "created_at": now, "updated_at": now},
                {"name": "Empreendedorismo", "slug": "empreendedorismo", "order": 4, "active": True, "created_at": now, "updated_at": now},
            ],
        )

    # Tabela permissions
    if not table_exists("permissions"):
        op.create_table(
            "permissions",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("codename", sa.String(50), unique=True, nullable=False),
            sa.Column("name", sa.String(100), nullable=False),
        )

        permissions_table = sa.table(
            "permissions",
            sa.column("codename", sa.String),
            sa.column("name", sa.String),
        )
        op.bulk_insert(
            permissions_table,
            [
                {"codename": "dashboard", "name": "Dashboard"},
                {"codename": "news", "name": "Notícias"},
                {"codename": "credit_lines", "name": "Linhas de Crédito"},
                {"codename": "categories", "name": "Categorias"},
                {"codename": "users", "name": "Usuários"},
                {"codename": "settings", "name": "Configurações"},
                {"codename": "reports", "name": "Relatórios"},
            ],
        )

    # Tabela user_permissions
    if not table_exists("user_permissions"):
        op.create_table(
            "user_permissions",
            sa.Column(
                "user_id",
                sa.Integer(),
                sa.ForeignKey("users.id", ondelete="CASCADE"),
                primary_key=True,
            ),
            sa.Column(
                "permission_id",
                sa.Integer(),
                sa.ForeignKey("permissions.id", ondelete="CASCADE"),
                primary_key=True,
            ),
        )

    # Coluna name na tabela users
    if not column_exists("users", "name"):
        op.add_column("users", sa.Column("name", sa.String(255), nullable=True))


def downgrade() -> None:
    if column_exists("users", "name"):
        op.drop_column("users", "name")
    if table_exists("user_permissions"):
        op.drop_table("user_permissions")
    if table_exists("permissions"):
        op.drop_table("permissions")
    if table_exists("categories"):
        op.drop_table("categories")
