from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SiteSettingResponse(BaseModel):
    id: int
    key: str
    value: bool
    label: str
    group: str
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SiteSettingUpdate(BaseModel):
    key: str
    value: bool


class SiteSettingBulkUpdate(BaseModel):
    settings: list[SiteSettingUpdate]
