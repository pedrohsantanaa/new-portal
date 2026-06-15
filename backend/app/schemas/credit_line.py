from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreditLineBase(BaseModel):
    title: str
    description: str
    details: Optional[str] = None
    icon_url: Optional[str] = None
    color: str = "#EEF4FF"
    order: int = 0
    active: bool = True


class CreditLineCreate(CreditLineBase):
    pass


class CreditLineUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    details: Optional[str] = None
    icon_url: Optional[str] = None
    color: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None


class CreditLineResponse(CreditLineBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreditLineListResponse(BaseModel):
    items: list[CreditLineResponse]
    total: int
    page: int
    pages: int
