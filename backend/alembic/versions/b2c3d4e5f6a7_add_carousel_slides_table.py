"""add carousel_slides table

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-07-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
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
    if not table_exists("carousel_slides"):
        op.create_table(
            "carousel_slides",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("image_url", sa.String(500), nullable=False),
            sa.Column("title", sa.String(200), nullable=True),
            sa.Column("description", sa.String(500), nullable=True),
            sa.Column("link", sa.String(500), nullable=True),
            sa.Column("btn_label", sa.String(100), nullable=True),
            sa.Column("btn_class", sa.String(50), server_default="btn-orange", nullable=False),
            sa.Column("order", sa.Integer(), server_default="0", nullable=False),
            sa.Column("active", sa.Boolean(), server_default="true", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

        slides_table = sa.table(
            "carousel_slides",
            sa.column("image_url", sa.String),
            sa.column("title", sa.String),
            sa.column("description", sa.String),
            sa.column("link", sa.String),
            sa.column("btn_label", sa.String),
            sa.column("btn_class", sa.String),
            sa.column("order", sa.Integer),
            sa.column("active", sa.Boolean),
            sa.column("created_at", sa.DateTime),
            sa.column("updated_at", sa.DateTime),
        )
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        op.bulk_insert(
            slides_table,
            [
                {"image_url": "/carroussel/b1.png", "title": None, "description": None, "link": "#", "btn_label": "Conheça Nossos Programas", "btn_class": "btn-orange", "order": 1, "active": True, "created_at": now, "updated_at": now},
                {"image_url": "/carroussel/b2.png", "title": None, "description": None, "link": "#", "btn_label": "Ver Dashboard", "btn_class": "btn-orange", "order": 2, "active": True, "created_at": now, "updated_at": now},
                {"image_url": "/carroussel/b3.png", "title": None, "description": None, "link": "#", "btn_label": "Localização", "btn_class": "btn-orange", "order": 3, "active": True, "created_at": now, "updated_at": now},
                {"image_url": "/carroussel/b8.png", "title": None, "description": None, "link": "#", "btn_label": "Renegociação de Dívidas", "btn_class": "btn-orange", "order": 4, "active": True, "created_at": now, "updated_at": now},
                {"image_url": "/carroussel/b5.png", "title": None, "description": None, "link": "#", "btn_label": "Compras Diretas", "btn_class": "btn-orange", "order": 5, "active": True, "created_at": now, "updated_at": now},
                {"image_url": "/carroussel/b6.png", "title": None, "description": None, "link": "#", "btn_label": "Saiba Mais", "btn_class": "btn-orange", "order": 6, "active": True, "created_at": now, "updated_at": now},
            ],
        )


def downgrade() -> None:
    if table_exists("carousel_slides"):
        op.drop_table("carousel_slides")
