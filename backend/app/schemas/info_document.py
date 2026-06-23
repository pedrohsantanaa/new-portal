from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InfoDocumentBase(BaseModel):
    title: str
    category_id: int
    file_url: str
    file_type: str
    file_size: Optional[int] = None
    year: int
    month: Optional[int] = None
    is_highlight: bool = False
    published: bool = False


class InfoDocumentCreate(InfoDocumentBase):
    pass


class InfoDocumentUpdate(BaseModel):
    title: Optional[str] = None
    category_id: Optional[int] = None
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    year: Optional[int] = None
    month: Optional[int] = None
    is_highlight: Optional[bool] = None
    published: Optional[bool] = None


class InfoDocumentResponse(InfoDocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None

    class Config:
        from_attributes = True


class InfoDocumentListResponse(BaseModel):
    items: list[InfoDocumentResponse]
    total: int
    page: int
    pages: int
