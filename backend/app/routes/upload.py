import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File, Form

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
}

ALL_ALLOWED_TYPES = {**ALLOWED_IMAGE_TYPES, **ALLOWED_DOC_TYPES}
MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5MB
MAX_DOC_SIZE = 10 * 1024 * 1024    # 10MB


@router.post("")
@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    folder: str = "general",
    # current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALL_ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo não permitido. Tipos aceitos: {', '.join(ALL_ALLOWED_TYPES.keys())}",
        )

    is_image = file.content_type in ALLOWED_IMAGE_TYPES
    max_size = MAX_IMAGE_SIZE if is_image else MAX_DOC_SIZE
    content = await file.read()

    if len(content) > max_size:
        size_label = "5MB" if is_image else "10MB"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Arquivo muito grande. Tamanho máximo: {size_label}",
        )

    ext = ALL_ALLOWED_TYPES[file.content_type]
    filename = f"{uuid.uuid4().hex}{ext}"
    upload_dir = Path(settings.UPLOAD_DIR) / folder
    upload_dir.mkdir(parents=True, exist_ok=True)
    filepath = upload_dir / filename

    with open(filepath, "wb") as f:
        f.write(content)

    return {
        "url": f"/uploads/{folder}/{filename}",
        "filename": filename,
        "content_type": file.content_type,
        "size": len(content),
    }
