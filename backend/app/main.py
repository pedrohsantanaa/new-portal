from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.routes import auth, news, credit_lines, upload

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Portal de Crédito - API",
    description="API para o Portal de Crédito do Tocantins",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(news.router, prefix="/api/news", tags=["News"])
app.include_router(credit_lines.router, prefix="/api/credit-lines", tags=["Credit Lines"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])


@app.get("/")
def root():
    return {"message": "Portal de Crédito API - Tocantins"}


@app.get("/health")
def health():
    return {"status": "ok"}
