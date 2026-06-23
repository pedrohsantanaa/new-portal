from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InfoCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 0


class InfoCategoryCreate(InfoCategoryBase):
    pass


class InfoCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None


class InfoCategoryResponse(InfoCategoryBase):
    id: int
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True


class InfoCategoryListResponse(BaseModel):
    items: list[InfoCategoryResponse]
    total: int
