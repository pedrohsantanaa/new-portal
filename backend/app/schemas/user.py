from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from app.schemas.permission import PermissionResponse


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    permission_ids: Optional[list[int]] = []

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not any(c.islower() for c in v):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("A senha deve conter pelo menos um número")
        return v


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    permission_ids: Optional[list[int]] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not any(c.islower() for c in v):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("A senha deve conter pelo menos um número")
        return v


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
