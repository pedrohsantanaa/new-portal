import uuid
import re
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    status,
    File,
    Request,
)

from app.config import settings
from app.models.user import User
from app.utils.deps import get_current_user

router = APIRouter()

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}

ALLOWED_DOC_TYPES = {
    "application/pdf": ".pdf",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "text/csv": ".csv",
}

ALL_ALLOWED_TYPES = {**ALLOWED_IMAGE_TYPES, **ALLOWED_DOC_TYPES}

MAGIC_BYTES = {
    "image/jpeg": [b"\xff\xd8\xff"],
    "image/png": [b"\x89PNG"],
    "image/webp": [b"RIFF"],
    "image/gif": [b"GIF8"],
    "application/pdf": [b"%PDF"],
    "application/msword": [b"\xd0\xcf\x11\xe0"],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [b"PK"],
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [b"PK"],
    "text/csv": [],
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_DOC_SIZE = 10 * 1024 * 1024   # 10 MB

SAFE_FOLDER_RE = re.compile(r"^[a-zA-Z0-9_\-]+$")


def verify_magic_bytes(content: bytes, content_type: str) -> bool:
    expected = MAGIC_BYTES.get(content_type)
    if expected is None:
        return False
    if not expected:
        return True
    return any(content[:len(prefix)] == prefix for prefix in expected)


@router.post("")
@router.post("/")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    folder: str = "general",
    current_user: User = Depends(get_current_user),
):
    if not SAFE_FOLDER_RE.match(folder):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de pasta inválido. Use apenas letras, números, hífens e underscores.",
        )

    if file.content_type not in ALL_ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Tipo de arquivo não permitido. "
                f"Tipos aceitos: {', '.join(ALL_ALLOWED_TYPES.keys())}"
            ),
        )

    is_image = file.content_type in ALLOWED_IMAGE_TYPES
    max_size = MAX_IMAGE_SIZE if is_image else MAX_DOC_SIZE

    content = await file.read()

    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Arquivo muito grande. "
                f"Tamanho máximo: {'5MB' if is_image else '10MB'}"
            ),
        )

    if not verify_magic_bytes(content, file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conteúdo do arquivo não corresponde ao tipo informado.",
        )

    extension = ALL_ALLOWED_TYPES[file.content_type]
    filename = f"{uuid.uuid4().hex}{extension}"

    upload_dir = Path(settings.UPLOAD_DIR) / folder
    upload_dir.mkdir(parents=True, exist_ok=True)

    filepath = upload_dir / filename

    with open(filepath, "wb") as f:
        f.write(content)

    return {
        "url": f"{request.base_url}uploads/{folder}/{filename}",
        "filename": filename,
        "content_type": file.content_type,
        "size": len(content),
    }
