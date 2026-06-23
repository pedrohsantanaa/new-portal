import math
import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdate,
)
from app.utils.deps import get_current_user, require_permission

router = APIRouter()


def generate_slug(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


@router.get("/", response_model=list[CategoryResponse])
def list_active_categories(db: Session = Depends(get_db)):
    categories = (
        db.query(Category)
        .filter(Category.active == True)
        .order_by(Category.order, Category.name)
        .all()
    )
    return categories


@router.get("/all", response_model=CategoryListResponse)
def list_all_categories(
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("categories")),
):
    query = db.query(Category)
    if search:
        query = query.filter(Category.name.ilike(f"%{search}%"))
    total = query.count()
    items = query.order_by(Category.order, Category.name).all()
    return CategoryListResponse(items=items, total=total)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("categories")),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("categories")),
):
    slug = generate_slug(data.name)
    existing = db.query(Category).filter(Category.slug == slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma categoria com este nome",
        )

    category = Category(
        name=data.name,
        slug=slug,
        description=data.description,
        active=data.active,
        order=data.order,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("categories")),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data:
        new_slug = generate_slug(update_data["name"])
        existing = (
            db.query(Category)
            .filter(Category.slug == new_slug, Category.id != category_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma categoria com este nome",
            )
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
    current_user: User = Depends(require_permission("categories")),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(category)
    db.commit()
