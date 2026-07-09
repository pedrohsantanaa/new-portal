"""add sale_items table

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-07-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, None] = "b2c3d4e5f6a7"
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
    if not table_exists("sale_items"):
        op.create_table(
            "sale_items",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("item_type", sa.String(20), nullable=False, index=True),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("description", sa.String(500), nullable=True),
            sa.Column("details", sa.Text(), nullable=True),
            sa.Column("city", sa.String(100), nullable=True, index=True),
            sa.Column("region", sa.String(100), nullable=True),
            sa.Column("property_type", sa.String(50), nullable=True),
            sa.Column("purpose", sa.String(100), nullable=True),
            sa.Column("year", sa.Integer(), nullable=True),
            sa.Column("fuel", sa.String(50), nullable=True),
            sa.Column("transmission", sa.String(50), nullable=True),
            sa.Column("price", sa.Numeric(12, 2), nullable=False),
            sa.Column("area_m2", sa.Integer(), nullable=True),
            sa.Column("image_url", sa.String(500), nullable=True),
            sa.Column("gallery", sa.Text(), nullable=True),
            sa.Column("phone", sa.String(20), nullable=True),
            sa.Column("featured", sa.Boolean(), server_default="false", nullable=False),
            sa.Column("active", sa.Boolean(), server_default="true", nullable=False),
            sa.Column("order", sa.Integer(), server_default="0", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

        items_table = sa.table(
            "sale_items",
            sa.column("item_type", sa.String),
            sa.column("title", sa.String),
            sa.column("description", sa.String),
            sa.column("details", sa.Text),
            sa.column("city", sa.String),
            sa.column("region", sa.String),
            sa.column("property_type", sa.String),
            sa.column("purpose", sa.String),
            sa.column("year", sa.Integer),
            sa.column("fuel", sa.String),
            sa.column("transmission", sa.String),
            sa.column("price", sa.Numeric),
            sa.column("area_m2", sa.Integer),
            sa.column("image_url", sa.String),
            sa.column("gallery", sa.Text),
            sa.column("phone", sa.String),
            sa.column("featured", sa.Boolean),
            sa.column("active", sa.Boolean),
            sa.column("order", sa.Integer),
            sa.column("created_at", sa.DateTime),
            sa.column("updated_at", sa.DateTime),
        )
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        op.bulk_insert(
            items_table,
            [
                {"item_type": "imovel", "title": "Palmas", "description": "Imóvel residencial urbano em Palmas", "details": None, "city": "Palmas", "region": None, "property_type": "Urbano", "purpose": "Residencial", "year": None, "fuel": None, "transmission": None, "price": 243000.00, "area_m2": 360, "image_url": None, "gallery": None, "phone": "(63) 99999-0001", "featured": True, "active": True, "order": 1, "created_at": now, "updated_at": now},
                {"item_type": "imovel", "title": "Porto Nacional", "description": "Imóvel residencial urbano em Porto Nacional", "details": None, "city": "Porto Nacional", "region": None, "property_type": "Urbano", "purpose": "Residencial", "year": None, "fuel": None, "transmission": None, "price": 225000.00, "area_m2": 300, "image_url": None, "gallery": None, "phone": "(63) 99999-0002", "featured": True, "active": True, "order": 2, "created_at": now, "updated_at": now},
                {"item_type": "imovel", "title": "Pedro Afonso", "description": "Imóvel residencial urbano em Pedro Afonso", "details": None, "city": "Pedro Afonso", "region": None, "property_type": "Urbano", "purpose": "Residencial", "year": None, "fuel": None, "transmission": None, "price": 252047.67, "area_m2": 450, "image_url": None, "gallery": None, "phone": "(63) 99999-0003", "featured": True, "active": True, "order": 3, "created_at": now, "updated_at": now},
                {"item_type": "imovel", "title": "Caseara", "description": "Imóvel residencial urbano em Caseara", "details": None, "city": "Caseara", "region": None, "property_type": "Rural", "purpose": "Residencial", "year": None, "fuel": None, "transmission": None, "price": 75000.00, "area_m2": 250, "image_url": None, "gallery": None, "phone": "(63) 99999-0004", "featured": True, "active": True, "order": 4, "created_at": now, "updated_at": now},
                {"item_type": "veiculo", "title": "Toyota Hilux SRX", "description": "Pick-up Toyota Hilux SRX 4x4", "details": None, "city": "Palmas", "region": None, "property_type": None, "purpose": None, "year": 2019, "fuel": "Diesel", "transmission": "Automática", "price": 145000.00, "area_m2": None, "image_url": None, "gallery": None, "phone": "(63) 99999-0005", "featured": True, "active": True, "order": 5, "created_at": now, "updated_at": now},
                {"item_type": "veiculo", "title": "Chevrolet Onix LT", "description": "Hatch Chevrolet Onix LT", "details": None, "city": "Porto Nacional", "region": None, "property_type": None, "purpose": None, "year": 2018, "fuel": "Flex", "transmission": "Manual", "price": 42500.00, "area_m2": None, "image_url": None, "gallery": None, "phone": "(63) 99999-0006", "featured": True, "active": True, "order": 6, "created_at": now, "updated_at": now},
                {"item_type": "veiculo", "title": "Jeep Renegade Sport", "description": "SUV Jeep Renegade Sport 4x4", "details": None, "city": "Palmas", "region": None, "property_type": None, "purpose": None, "year": 2016, "fuel": "Flex", "transmission": "Automática", "price": 56000.00, "area_m2": None, "image_url": None, "gallery": None, "phone": "(63) 99999-0007", "featured": True, "active": True, "order": 7, "created_at": now, "updated_at": now},
                {"item_type": "veiculo", "title": "Honda CG 160 Titan", "description": "Motocicleta Honda CG 160 Titan", "details": None, "city": "Araguaína", "region": None, "property_type": None, "purpose": None, "year": 2020, "fuel": "Flex", "transmission": "Manual", "price": 12000.00, "area_m2": None, "image_url": None, "gallery": None, "phone": "(63) 99999-0008", "featured": True, "active": True, "order": 8, "created_at": now, "updated_at": now},
            ],
        )


def downgrade() -> None:
    if table_exists("sale_items"):
        op.drop_table("sale_items")
