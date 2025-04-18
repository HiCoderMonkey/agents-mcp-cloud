from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.config import settings
from app.core.security import get_password_hash
from app.utils import (
    generate_password_reset_token,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 兼容的令牌登录，获取访问令牌给未来的API调用
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/json-login", response_model=schemas.Token)
def login_json(
    db: Session = Depends(deps.get_db), login_data: schemas.LoginJson = Body(...)
) -> Any:
    """
    JSON格式的登录API，接受用户名和密码字段
    """
    user = crud.user.authenticate(
        db, email=login_data.username, password=login_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "user": user
    }


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    密码恢复
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="找不到使用该电子邮件的用户",
        )
    password_reset_token = generate_password_reset_token(email=email)
    # 发送重置密码邮件 (这里需要实现)
    # send_reset_password_email(
    #     email_to=user.email, email=email, token=password_reset_token
    # )
    return {"msg": "密码恢复邮件已发送"}


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    重置密码
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="无效的令牌")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="找不到使用该电子邮件的用户",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="未激活的用户")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "密码更新成功"} 