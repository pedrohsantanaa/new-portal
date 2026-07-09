from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CarouselSlideBase(BaseModel):
    image_url: str
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    btn_label: Optional[str] = None
    btn_class: str = "btn-orange"
    order: int = 0
    active: bool = True


class CarouselSlideCreate(CarouselSlideBase):
    pass


class CarouselSlideUpdate(BaseModel):
    image_url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    btn_label: Optional[str] = None
    btn_class: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None


class CarouselSlideResponse(CarouselSlideBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CarouselSlideListResponse(BaseModel):
    items: list[CarouselSlideResponse]
    total: int
