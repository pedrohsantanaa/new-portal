from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreditLineDocument(BaseModel):
    url: str
    label: str


class CreditLineBase(BaseModel):
    title: str
    description: str
    details: Optional[str] = None
    icon_url: Optional[str] = None
    color: str = "#EEF4FF"
    order: int = 0
    active: bool = True
    documents: Optional[list[CreditLineDocument]] = None
    authorization_text: Optional[str] = None
    external_html: Optional[str] = None


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
    documents: Optional[list[CreditLineDocument]] = None
    authorization_text: Optional[str] = None
    external_html: Optional[str] = None


class CreditLineResponse(CreditLineBase):
    id: int
    slug: str
    documents: Optional[list[CreditLineDocument]] = None
    authorization_text: Optional[str] = None
    external_html: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreditLineListResponse(BaseModel):
    items: list[CreditLineResponse]
    total: int
    page: int
    pages: int
