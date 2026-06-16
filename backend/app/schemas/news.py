from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    category: str
    summary: str
    content: str
    image_url: Optional[str] = None
    published: bool = False
    slug: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    visibility: str = "public"
    scheduled_at: Optional[datetime] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    published: Optional[bool] = None
    slug: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    visibility: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None


class NewsResponse(NewsBase):
    id: int
    slug: str
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NewsListResponse(BaseModel):
    items: list[NewsResponse]
    total: int
    page: int
    pages: int
