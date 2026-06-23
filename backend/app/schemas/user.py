from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.permission import PermissionResponse


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    permission_ids: Optional[list[int]] = []


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    permission_ids: Optional[list[int]] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    permissions: list[PermissionResponse] = []

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str
