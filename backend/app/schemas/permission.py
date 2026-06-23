from pydantic import BaseModel


class PermissionResponse(BaseModel):
    id: int
    codename: str
    name: str

    class Config:
        from_attributes = True
