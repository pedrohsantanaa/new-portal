import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import distinct, func

from app.database import get_db
from app.models.info_category import InfoCategory
from app.models.info_document import InfoDocument
from app.models.user import User
from app.schemas.info_document import (
    InfoDocumentCreate,
    InfoDocumentListResponse,
    InfoDocumentResponse,
    InfoDocumentUpdate,
)
from app.utils.deps import require_permission

router = APIRouter()


@router.get("/public", response_model=InfoDocumentListResponse)
def list_public_documents(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    category_slug: str = Query(None),
    year: int = Query(None),
    search: str = Query(None),
    highlight_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    query = db.query(InfoDocument).filter(InfoDocument.published == True)

    if category_slug:
        cat = db.query(InfoCategory).filter(InfoCategory.slug == category_slug).first()
        if cat:
            query = query.filter(InfoDocument.category_id == cat.id)

    if year:
        query = query.filter(InfoDocument.year == year)

    if search:
        query = query.filter(InfoDocument.title.ilike(f"%{search}%"))

    if highlight_only:
        query = query.filter(InfoDocument.is_highlight == True)

    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 1
    items = (
        query.order_by(InfoDocument.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    result = []
    for doc in items:
        result.append(InfoDocumentResponse(
            id=doc.id,
            title=doc.title,
            category_id=doc.category_id,
            file_url=doc.file_url,
            file_type=doc.file_type,
            file_size=doc.file_size,
            year=doc.year,
            month=doc.month,
            is_highlight=doc.is_highlight,
            published=doc.published,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            category_name=doc.category.name if doc.category else None,
        ))

    return InfoDocumentListResponse(items=result, total=total, page=page, pages=pages)


@router.get("/years")
def list_years(db: Session = Depends(get_db)):
    rows = (
        db.query(distinct(InfoDocument.year))
        .filter(InfoDocument.published == True)
        .order_by(InfoDocument.year.desc())
        .all()
    )
    return {"years": [r[0] for r in rows]}


@router.get("/all", response_model=InfoDocumentListResponse)
def list_all_documents(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    search: str = Query(None),
    category_id: int = Query(None),
    year: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    query = db.query(InfoDocument)

    if search:
        query = query.filter(InfoDocument.title.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(InfoDocument.category_id == category_id)
    if year:
        query = query.filter(InfoDocument.year == year)

    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 1
    items = (
        query.order_by(InfoDocument.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    result = []
    for doc in items:
        result.append(InfoDocumentResponse(
            id=doc.id,
            title=doc.title,
            category_id=doc.category_id,
            file_url=doc.file_url,
            file_type=doc.file_type,
            file_size=doc.file_size,
            year=doc.year,
            month=doc.month,
            is_highlight=doc.is_highlight,
            published=doc.published,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            category_name=doc.category.name if doc.category else None,
        ))

    return InfoDocumentListResponse(items=result, total=total, page=page, pages=pages)


@router.get("/{document_id}", response_model=InfoDocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    doc = db.query(InfoDocument).filter(InfoDocument.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return InfoDocumentResponse(
        id=doc.id,
        title=doc.title,
        category_id=doc.category_id,
        file_url=doc.file_url,
        file_type=doc.file_type,
        file_size=doc.file_size,
        year=doc.year,
        month=doc.month,
        is_highlight=doc.is_highlight,
        published=doc.published,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        category_name=doc.category.name if doc.category else None,
    )


@router.post("/", response_model=InfoDocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(
    data: InfoDocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    cat = db.query(InfoCategory).filter(InfoCategory.id == data.category_id).first()
    if not cat:
        raise HTTPException(status_code=400, detail="Categoria não encontrada")

    doc = InfoDocument(**data.model_dump())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return InfoDocumentResponse(
        id=doc.id,
        title=doc.title,
        category_id=doc.category_id,
        file_url=doc.file_url,
        file_type=doc.file_type,
        file_size=doc.file_size,
        year=doc.year,
        month=doc.month,
        is_highlight=doc.is_highlight,
        published=doc.published,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        category_name=cat.name,
    )


@router.put("/{document_id}", response_model=InfoDocumentResponse)
def update_document(
    document_id: int,
    data: InfoDocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    doc = db.query(InfoDocument).filter(InfoDocument.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    update_data = data.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        cat = db.query(InfoCategory).filter(InfoCategory.id == update_data["category_id"]).first()
        if not cat:
            raise HTTPException(status_code=400, detail="Categoria não encontrada")

    for key, value in update_data.items():
        setattr(doc, key, value)

    db.commit()
    db.refresh(doc)
    return InfoDocumentResponse(
        id=doc.id,
        title=doc.title,
        category_id=doc.category_id,
        file_url=doc.file_url,
        file_type=doc.file_type,
        file_size=doc.file_size,
        year=doc.year,
        month=doc.month,
        is_highlight=doc.is_highlight,
        published=doc.published,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        category_name=doc.category.name if doc.category else None,
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("info_access")),
):
    doc = db.query(InfoDocument).filter(InfoDocument.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    db.delete(doc)
    db.commit()
