from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class InfoDocument(Base):
    __tablename__ = "info_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    category_id = Column(Integer, ForeignKey("info_categories.id"), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_type = Column(String(10), nullable=False)
    file_size = Column(Integer, nullable=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=True)
    is_highlight = Column(Boolean, default=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    category = relationship("InfoCategory", backref="documents")

    def __repr__(self):
        return f"<InfoDocument {self.title}>"
