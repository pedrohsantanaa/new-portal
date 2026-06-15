import math
import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.credit_line import CreditLine
from app.models.user import User
from app.schemas.credit_line import (
    CreditLineCreate,
    CreditLineListResponse,
    CreditLineResponse,
    CreditLineUpdate,
)
from app.utils.deps import get_current_user

router = APIRouter()


def generate_slug(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


@router.get("/", response_model=CreditLineListResponse)
def list_credit_lines(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    active_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    query = db.query(CreditLine)
    if active_only:
        query = query.filter(CreditLine.active == True)
    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 1
    items = (
        query.order_by(CreditLine.order, CreditLine.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return CreditLineListResponse(items=items, total=total, page=page, pages=pages)


@router.get("/{slug}", response_model=CreditLineResponse)
def get_credit_line(slug: str, db: Session = Depends(get_db)):
    credit_line = db.query(CreditLine).filter(CreditLine.slug == slug).first()
    if not credit_line:
        raise HTTPException(status_code=404, detail="Linha de crédito não encontrada")
    return credit_line


@router.post("/", response_model=CreditLineResponse, status_code=status.HTTP_201_CREATED)
def create_credit_line(
    data: CreditLineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    slug = generate_slug(data.title)
    existing = db.query(CreditLine).filter(CreditLine.slug == slug).first()
    if existing:
        slug = f"{slug}-{int(datetime.now(timezone.utc).timestamp())}"
    credit_line = CreditLine(
        title=data.title,
        slug=slug,
        description=data.description,
        details=data.details,
        icon_url=data.icon_url,
        color=data.color,
        order=data.order,
        active=data.active,
    )
    db.add(credit_line)
    db.commit()
    db.refresh(credit_line)
    return credit_line


@router.put("/{credit_line_id}", response_model=CreditLineResponse)
def update_credit_line(
    credit_line_id: int,
    data: CreditLineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    credit_line = db.query(CreditLine).filter(CreditLine.id == credit_line_id).first()
    if not credit_line:
        raise HTTPException(status_code=404, detail="Linha de crédito não encontrada")
    update_data = data.model_dump(exclude_unset=True)
    if "title" in update_data:
        update_data["slug"] = generate_slug(update_data["title"])
    for key, value in update_data.items():
        setattr(credit_line, key, value)
    db.commit()
    db.refresh(credit_line)
    return credit_line


@router.delete("/{credit_line_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_credit_line(
    credit_line_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    credit_line = db.query(CreditLine).filter(CreditLine.id == credit_line_id).first()
    if not credit_line:
        raise HTTPException(status_code=404, detail="Linha de crédito não encontrada")
    db.delete(credit_line)
    db.commit()
