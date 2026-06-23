import re

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.info_category import InfoCategory
from app.models.user import User
from app.schemas.info_category import (
    InfoCategoryCreate,
    InfoCategoryListResponse,
    InfoCategoryResponse,
    InfoCategoryUpdate,
)
from app.utils.deps import require_permission

router = APIRouter()


def generate_slug(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


@router.get("/", response_model=InfoCategoryListResponse)
def list_categories(
    search: str = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(InfoCategory)
    if search:
        query = query.filter(InfoCategory.name.ilike(f"%{search}%"))
    categories = query.order_by(InfoCategory.sort_order, InfoCategory.name).all()
    return InfoCategoryListResponse(items=categories, total=len(categories))


@router.get("/all", response_model=InfoCategoryListResponse)
def list_all_categories(
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    query = db.query(InfoCategory)
    if search:
        query = query.filter(InfoCategory.name.ilike(f"%{search}%"))
    categories = query.order_by(InfoCategory.sort_order, InfoCategory.name).all()
    return InfoCategoryListResponse(items=categories, total=len(categories))


@router.get("/{category_id}", response_model=InfoCategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    category = db.query(InfoCategory).filter(InfoCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category


@router.post("/", response_model=InfoCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: InfoCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    slug = generate_slug(data.name)
    existing = db.query(InfoCategory).filter(InfoCategory.slug == slug).first()
    if existing:
        slug = f"{slug}-{int(__import__('time').time())}"

    category = InfoCategory(
        name=data.name,
        slug=slug,
        description=data.description,
        icon=data.icon,
        sort_order=data.sort_order,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=InfoCategoryResponse)
def update_category(
    category_id: int,
    data: InfoCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    category = db.query(InfoCategory).filter(InfoCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data:
        new_slug = generate_slug(update_data["name"])
        existing = db.query(InfoCategory).filter(
            InfoCategory.slug == new_slug, InfoCategory.id != category_id
        ).first()
        if existing:
            new_slug = f"{new_slug}-{int(__import__('time').time())}"
        update_data["slug"] = new_slug

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    category = db.query(InfoCategory).filter(InfoCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(category)
    db.commit()
