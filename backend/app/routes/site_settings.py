from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.site_setting import SiteSetting
from app.models.user import User
from app.schemas.site_setting import (
    SiteSettingBulkUpdate,
    SiteSettingResponse,
)
from app.utils.deps import get_current_user, require_permission

router = APIRouter()


@router.get("/public", response_model=list[SiteSettingResponse])
def get_public_settings(db: Session = Depends(get_db)):
    settings = (
        db.query(SiteSetting)
        .order_by(SiteSetting.group, SiteSetting.order)
        .all()
    )
    return settings


@router.get("/", response_model=list[SiteSettingResponse])
def list_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    settings = (
        db.query(SiteSetting)
        .order_by(SiteSetting.group, SiteSetting.order)
        .all()
    )
    return settings


@router.put("/", response_model=list[SiteSettingResponse])
def update_settings(
    data: SiteSettingBulkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings")),
):
    settings_map = {s.key: s for s in db.query(SiteSetting).all()}

    for item in data.settings:
        setting = settings_map.get(item.key)
        if setting:
            setting.value = item.value

    db.commit()

    settings = (
        db.query(SiteSetting)
        .order_by(SiteSetting.group, SiteSetting.order)
        .all()
    )
    return settings
