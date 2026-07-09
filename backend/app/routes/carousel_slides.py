from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.carousel_slide import CarouselSlide
from app.models.user import User
from app.schemas.carousel_slide import (
    CarouselSlideCreate,
    CarouselSlideListResponse,
    CarouselSlideResponse,
    CarouselSlideUpdate,
)
from app.utils.deps import get_current_user, require_permission

router = APIRouter()


@router.get("/public", response_model=list[CarouselSlideResponse])
def get_public_slides(db: Session = Depends(get_db)):
    slides = (
        db.query(CarouselSlide)
        .filter(CarouselSlide.active == True)
        .order_by(CarouselSlide.order)
        .all()
    )
    return slides


@router.get("/", response_model=CarouselSlideListResponse)
def list_all_slides(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    slides = (
        db.query(CarouselSlide)
        .order_by(CarouselSlide.order)
        .all()
    )
    return CarouselSlideListResponse(items=slides, total=len(slides))


@router.get("/{slide_id}", response_model=CarouselSlideResponse)
def get_slide(
    slide_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    slide = db.query(CarouselSlide).filter(CarouselSlide.id == slide_id).first()
    if not slide:
        raise HTTPException(status_code=404, detail="Slide não encontrado")
    return slide


@router.post("/", response_model=CarouselSlideResponse, status_code=status.HTTP_201_CREATED)
def create_slide(
    data: CarouselSlideCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    slide = CarouselSlide(
        image_url=data.image_url,
        title=data.title,
        description=data.description,
        link=data.link,
        btn_label=data.btn_label,
        btn_class=data.btn_class,
        order=data.order,
        active=data.active,
    )
    db.add(slide)
    db.commit()
    db.refresh(slide)
    return slide


@router.put("/{slide_id}", response_model=CarouselSlideResponse)
def update_slide(
    slide_id: int,
    data: CarouselSlideUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    slide = db.query(CarouselSlide).filter(CarouselSlide.id == slide_id).first()
    if not slide:
        raise HTTPException(status_code=404, detail="Slide não encontrado")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(slide, key, value)

    db.commit()
    db.refresh(slide)
    return slide


@router.delete("/{slide_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slide(
    slide_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    slide = db.query(CarouselSlide).filter(CarouselSlide.id == slide_id).first()
    if not slide:
        raise HTTPException(status_code=404, detail="Slide não encontrado")
    db.delete(slide)
    db.commit()
