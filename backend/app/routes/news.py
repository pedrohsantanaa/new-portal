import math
import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.news import News
from app.models.user import User
from app.schemas.news import (
    NewsCreate,
    NewsListResponse,
    NewsResponse,
    NewsUpdate,
)
from app.utils.deps import get_current_user

router = APIRouter()


def generate_slug(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


@router.get("/", response_model=NewsListResponse)
def list_news(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    category: str = Query(None),
    published_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    query = db.query(News)
    if published_only:
        query = query.filter(News.published == True)
    if category:
        query = query.filter(News.category == category)
    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 1
    items = (
        query.order_by(News.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return NewsListResponse(items=items, total=total, page=page, pages=pages)


@router.get("/{slug}", response_model=NewsResponse)
def get_news(slug: str, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.slug == slug).first()
    if not news:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return news


@router.post("/", response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
def create_news(
    data: NewsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    slug = generate_slug(data.title)
    existing = db.query(News).filter(News.slug == slug).first()
    if existing:
        slug = f"{slug}-{int(datetime.now(timezone.utc).timestamp())}"
    news = News(
        title=data.title,
        slug=slug,
        category=data.category,
        summary=data.summary,
        content=data.content,
        image_url=data.image_url,
        published=data.published,
        published_at=datetime.now(timezone.utc) if data.published else None,
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


@router.put("/{news_id}", response_model=NewsResponse)
def update_news(
    news_id: int,
    data: NewsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    update_data = data.model_dump(exclude_unset=True)
    if "title" in update_data:
        update_data["slug"] = generate_slug(update_data["title"])
    if "published" in update_data and update_data["published"] and not news.published:
        update_data["published_at"] = datetime.now(timezone.utc)
    for key, value in update_data.items():
        setattr(news, key, value)
    db.commit()
    db.refresh(news)
    return news


@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    db.delete(news)
    db.commit()
