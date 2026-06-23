"""add info_access tables

Revision ID: e1f2g3h4i5j6
Revises: d4e5f6a7b8c9
Create Date: 2026-06-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e1f2g3h4i5j6"
down_revision: Union[str, None] = "d4e5f6a7b8c9"
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
    # Tabela info_categories
    if not table_exists("info_categories"):
        op.create_table(
            "info_categories",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(200), nullable=False),
            sa.Column("slug", sa.String(200), unique=True, nullable=False, index=True),
            sa.Column("description", sa.String(500), nullable=True),
            sa.Column("icon", sa.String(50), nullable=True),
            sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        )

        # Categorias padrão de acesso à informação
        info_categories_table = sa.table(
            "info_categories",
            sa.column("name", sa.String),
            sa.column("slug", sa.String),
            sa.column("description", sa.String),
            sa.column("icon", sa.String),
            sa.column("sort_order", sa.Integer),
            sa.column("created_at", sa.DateTime),
        )
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        op.bulk_insert(
            info_categories_table,
            [
                {"name": "Políticas, Manuais e Resoluções", "slug": "politicas-manuais-e-resolucoes", "description": "Aceça políticas, manuais e resoluções institucionais.", "icon": "file-text", "sort_order": 1, "created_at": now},
                {"name": "Relatórios", "slug": "relatorios", "description": "Relatórios administrativos, de gestão e de atividades.", "icon": "bar-chart-3", "sort_order": 2, "created_at": now},
                {"name": "Financeiro e Contábil", "slug": "financeiro-e-contabil", "description": "Despesas, execuções, balanços e demonstrações financeiras.", "icon": "calculator", "sort_order": 3, "created_at": now},
                {"name": "Organograma", "slug": "organograma", "description": "Estrutura organizacional da Agência de Fomento.", "icon": "network", "sort_order": 4, "created_at": now},
                {"name": "Editais", "slug": "editais", "description": "Editais de chamamento, contratações e avisos.", "icon": "megaphone", "sort_order": 5, "created_at": now},
                {"name": "Gestão de Riscos", "slug": "gestao-de-riscos", "description": "Políticas e relatórios de gestão de riscos.", "icon": "shield-check", "sort_order": 6, "created_at": now},
                {"name": "Concursos", "slug": "concursos", "description": "Editais, resultados e informações de concursos.", "icon": "users", "sort_order": 7, "created_at": now},
                {"name": "Legislação", "slug": "legislacao", "description": "Leis, decretos, portarias e normas aplicáveis.", "icon": "scale", "sort_order": 8, "created_at": now},
            ],
        )

    # Tabela info_documents
    if not table_exists("info_documents"):
        op.create_table(
            "info_documents",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("title", sa.String(300), nullable=False),
            sa.Column("category_id", sa.Integer(), sa.ForeignKey("info_categories.id"), nullable=False),
            sa.Column("file_url", sa.String(500), nullable=False),
            sa.Column("file_type", sa.String(10), nullable=False),
            sa.Column("file_size", sa.Integer(), nullable=True),
            sa.Column("year", sa.Integer(), nullable=False),
            sa.Column("month", sa.Integer(), nullable=True),
            sa.Column("is_highlight", sa.Boolean(), server_default="false", nullable=False),
            sa.Column("published", sa.Boolean(), server_default="false", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # Adicionar permissão info_access
    if not table_exists("permissions") or True:
        try:
            op.execute(
                "INSERT INTO permissions (codename, name) VALUES ('info_access', 'Acesso à Informação') "
                "ON CONFLICT (codename) DO NOTHING"
            )
        except Exception:
            pass


def downgrade() -> None:
    if table_exists("info_documents"):
        op.drop_table("info_documents")
    if table_exists("info_categories"):
        op.drop_table("info_categories")
