import pyotp
import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.permission import Permission
from app.models.user import User
from app.schemas.permission import PermissionResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.auth import TOTPSetupResponse, TOTPEnableRequest
from app.utils.auth import hash_password
from app.utils.deps import get_current_user, require_permission

router = APIRouter()

TOTP_ISSUER = getattr(settings, "TOTP_ISSUER_NAME", "Portal de Credito")


@router.get("/", response_model=list[UserResponse])
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users")),
):
    query = db.query(User)
    if search:
        query = query.filter(
            User.email.ilike(f"%{search}%") | User.name.ilike(f"%{search}%")
        )
    users = (
        query.order_by(User.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return users


@router.get("/permissions", response_model=list[PermissionResponse])
def list_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users")),
):
    permissions = db.query(Permission).order_by(Permission.codename).all()
    return permissions


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users")),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users")),
):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ja existe um usuario com este e-mail",
        )

    permissions = []
    if data.permission_ids:
        permissions = (
            db.query(Permission).filter(Permission.id.in_(data.permission_ids)).all()
        )

    user = User(
        email=data.email,
        name=data.name,
        hashed_password=hash_password(data.password),
        is_active=True,
        permissions=permissions,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users")),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    update_data = data.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] != user.email:
        existing = (
            db.query(User)
            .filter(User.email == update_data["email"], User.id != user_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ja existe um usuario com este e-mail",
            )

    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    else:
        update_data.pop("password", None)

    if "permission_ids" in update_data:
        permission_ids = update_data.pop("permission_ids")
        if permission_ids is not None:
            permissions = (
                db.query(Permission)
                .filter(Permission.id.in_(permission_ids))
                .all()
            )
            user.permissions = permissions

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users")),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Voce nao pode excluir seu proprio usuario",
        )
    db.delete(user)
    db.commit()


@router.post("/{user_id}/setup-2fa", response_model=TOTPSetupResponse)
def setup_2fa(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users")),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    otpauth_url = totp.provisioning_uri(name=user.email, issuer_name=TOTP_ISSUER)

    user.totp_secret = secret
    db.commit()

    return TOTPSetupResponse(secret=secret, otpauth_url=otpauth_url)


@router.post("/{user_id}/verify-2fa")
def verify_user_2fa(
    user_id: int,
    body: TOTPEnableRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users")),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    if not user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Execute setup-2fa primeiro",
        )

    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(body.code, valid_window=1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Codigo invalido. Tente novamente.",
        )

    user.two_factor_enabled = True
    db.commit()

    return {"success": True, "message": "2FA ativado com sucesso"}


@router.post("/{user_id}/disable-2fa")
def disable_2fa(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users")),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    user.two_factor_enabled = False
    user.totp_secret = None
    db.commit()

    return {"success": True, "message": "2FA desativado com sucesso"}
