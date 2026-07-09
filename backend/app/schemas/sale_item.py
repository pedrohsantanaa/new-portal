from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SaleItemBase(BaseModel):
    item_type: str
    title: str
    description: Optional[str] = None
    details: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    property_type: Optional[str] = None
    purpose: Optional[str] = None
    year: Optional[int] = None
    fuel: Optional[str] = None
    transmission: Optional[str] = None
    price: float
    area_m2: Optional[int] = None
    image_url: Optional[str] = None
    gallery: Optional[str] = None
    phone: Optional[str] = None
    featured: bool = False
    active: bool = True
    order: int = 0


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(BaseModel):
    item_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    details: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    property_type: Optional[str] = None
    purpose: Optional[str] = None
    year: Optional[int] = None
    fuel: Optional[str] = None
    transmission: Optional[str] = None
    price: Optional[float] = None
    area_m2: Optional[int] = None
    image_url: Optional[str] = None
    gallery: Optional[str] = None
    phone: Optional[str] = None
    featured: Optional[bool] = None
    active: Optional[bool] = None
    order: Optional[int] = None


class SaleItemResponse(SaleItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SaleItemListResponse(BaseModel):
    items: list[SaleItemResponse]
    total: int
    page: int
    pages: int
