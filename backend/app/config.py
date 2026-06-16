from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/portal_db"
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    UPLOAD_DIR: str = "uploads"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:5174"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

if not settings.UPLOAD_DIR or not Path(settings.UPLOAD_DIR).is_absolute():
    settings.UPLOAD_DIR = str(BASE_DIR / "uploads")
