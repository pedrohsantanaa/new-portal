from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database import Base


class CarouselSlide(Base):
    __tablename__ = "carousel_slides"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500), nullable=False)
    title = Column(String(200), nullable=True)
    description = Column(String(500), nullable=True)
    link = Column(String(500), nullable=True)
    btn_label = Column(String(100), nullable=True)
    btn_class = Column(String(50), default="btn-orange")
    order = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<CarouselSlide {self.title or self.id}>"
