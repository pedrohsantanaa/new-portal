from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text

from app.database import Base


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String(20), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    details = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    region = Column(String(100), nullable=True)
    property_type = Column(String(50), nullable=True)
    purpose = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    fuel = Column(String(50), nullable=True)
    transmission = Column(String(50), nullable=True)
    price = Column(Numeric(12, 2), nullable=False)
    area_m2 = Column(Integer, nullable=True)
    image_url = Column(String(500), nullable=True)
    gallery = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    featured = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<SaleItem {self.title}>"
