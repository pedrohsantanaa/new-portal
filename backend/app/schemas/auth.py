from typing import Optional

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class TokenPending(BaseModel):
    pending_token: str
    requires_2fa: bool = True


class TOTPVerifyRequest(BaseModel):
    pending_token: str
    code: str


class TOTPSetupResponse(BaseModel):
    secret: str
    otpauth_url: str


class TOTPEnableRequest(BaseModel):
    code: str


class TOTPDisableRequest(BaseModel):
    pass


class TOTPLoginRequest(BaseModel):
    pending_token: str
    code: str
