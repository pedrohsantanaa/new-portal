import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.routes import auth, news, credit_lines, upload, categories, users, info_categories, info_documents, site_settings, carousel_slides, sale_items

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Portal de Crédito - API",
    description="API para o Portal de Crédito do Tocantins",
    version="1.0.0",
    debug=settings.DEBUG,
)

origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NoCacheAPIMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/api"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, proxy-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            response.headers["Surrogate-Control"] = "no-store"
        return response


app.add_middleware(NoCacheAPIMiddleware)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"},
    )


app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(news.router, prefix="/api/news", tags=["News"])
app.include_router(credit_lines.router, prefix="/api/credit-lines", tags=["Credit Lines"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(info_categories.router, prefix="/api/info-categories", tags=["Info Categories"])
app.include_router(info_documents.router, prefix="/api/info-documents", tags=["Info Documents"])
app.include_router(site_settings.router, prefix="/api/site-settings", tags=["Site Settings"])
app.include_router(carousel_slides.router, prefix="/api/carousel-slides", tags=["Carousel Slides"])
app.include_router(sale_items.router, prefix="/api/sale-items", tags=["Sale Items"])


@app.get("/")
def root():
    return {"message": "Portal de Crédito API - Tocantins"}


@app.get("/health")
def health():
    return {"status": "ok"}
