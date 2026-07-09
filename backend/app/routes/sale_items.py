import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.sale_item import SaleItem
from app.models.user import User
from app.schemas.sale_item import (
    SaleItemCreate,
    SaleItemListResponse,
    SaleItemResponse,
    SaleItemUpdate,
)
from app.utils.deps import get_current_user, require_permission

router = APIRouter()


@router.get("/public", response_model=SaleItemListResponse)
def list_public_items(
    item_type: str = Query(None),
    property_type: str = Query(None),
    purpose: str = Query(None),
    city: str = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(SaleItem).filter(SaleItem.active == True)

    if item_type:
        query = query.filter(SaleItem.item_type == item_type)
    if property_type:
        query = query.filter(SaleItem.property_type == property_type)
    if purpose:
        query = query.filter(SaleItem.purpose == purpose)
    if city:
        query = query.filter(SaleItem.city.ilike(f"%{city}%"))
    if search:
        query = query.filter(
            SaleItem.title.ilike(f"%{search}%")
            | SaleItem.city.ilike(f"%{search}%")
            | SaleItem.description.ilike(f"%{search}%")
        )

    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 1
    items = (
        query.order_by(SaleItem.featured.desc(), SaleItem.order, SaleItem.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return SaleItemListResponse(items=items, total=total, page=page, pages=pages)


@router.get("/public/featured", response_model=list[SaleItemResponse])
def get_featured_items(
    item_type: str = Query(None),
    limit: int = Query(4, ge=1, le=12),
    db: Session = Depends(get_db),
):
    query = db.query(SaleItem).filter(SaleItem.active == True, SaleItem.featured == True)
    if item_type:
        query = query.filter(SaleItem.item_type == item_type)
    items = query.order_by(SaleItem.order).limit(limit).all()
    return items


@router.get("/public/stats")
def get_stats(db: Session = Depends(get_db)):
    imoveis = (
        db.query(func.count(SaleItem.id))
        .filter(SaleItem.active == True, SaleItem.item_type == "imovel")
        .scalar()
    )
    veiculos = (
        db.query(func.count(SaleItem.id))
        .filter(SaleItem.active == True, SaleItem.item_type == "veiculo")
        .scalar()
    )
    return {"imoveis": imoveis, "veiculos": veiculos}


@router.get("/", response_model=SaleItemListResponse)
def list_all_items(
    item_type: str = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    query = db.query(SaleItem)

    if item_type:
        query = query.filter(SaleItem.item_type == item_type)
    if search:
        query = query.filter(
            SaleItem.title.ilike(f"%{search}%")
            | SaleItem.city.ilike(f"%{search}%")
        )

    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 1
    items = (
        query.order_by(SaleItem.order, SaleItem.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return SaleItemListResponse(items=items, total=total, page=page, pages=pages)


@router.get("/{item_id}", response_model=SaleItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    item = db.query(SaleItem).filter(SaleItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


@router.post("/", response_model=SaleItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    data: SaleItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    item = SaleItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=SaleItemResponse)
def update_item(
    item_id: int,
    data: SaleItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    item = db.query(SaleItem).filter(SaleItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    item = db.query(SaleItem).filter(SaleItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(item)
    db.commit()
