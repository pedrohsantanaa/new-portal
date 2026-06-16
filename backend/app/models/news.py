from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False)
    summary = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    author = Column(String(255), nullable=True)
    tags = Column(JSON, nullable=True)
    categories = Column(JSON, nullable=True)
    visibility = Column(String(20), default="public")
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    seo_title = Column(String(255), nullable=True)
    seo_description = Column(String(300), nullable=True)
    seo_keywords = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<News {self.title}>"
