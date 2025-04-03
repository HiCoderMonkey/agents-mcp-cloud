import uuid
from typing import Any, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.SDKKey])
def read_sdk_keys(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取SDK密钥列表
    """
    if current_user.is_admin:
        sdk_keys = crud.sdk_key.get_multi(db, skip=skip, limit=limit)
    else:
        # 获取用户的Agent关联的SDK密钥
        sdk_keys = crud.sdk_key.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return sdk_keys


@router.post("/", response_model=schemas.SDKKey)
def create_sdk_key(
    *,
    db: Session = Depends(deps.get_db),
    sdk_key_in: schemas.SDKKeyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新的SDK密钥
    """
    # 检查Agent是否存在
    agent = crud.agent.get(db=db, id=sdk_key_in.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent不存在")
    if not current_user.is_admin and (agent.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    
    # 生成唯一密钥
    key = f"sdk_{uuid.uuid4().hex}"
    
    # 设置过期时间（30天）
    expires_at = datetime.utcnow() + timedelta(days=30)
    
    # 创建SDK密钥
    sdk_key = crud.sdk_key.create_with_key(
        db=db, 
        obj_in=sdk_key_in, 
        key=key,
        expires_at=expires_at
    )
    return sdk_key


@router.get("/{sdk_key_id}", response_model=schemas.SDKKey)
def read_sdk_key(
    *,
    db: Session = Depends(deps.get_db),
    sdk_key_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过ID获取SDK密钥
    """
    sdk_key = crud.sdk_key.get(db=db, id=sdk_key_id)
    if not sdk_key:
        raise HTTPException(status_code=404, detail="SDK密钥不存在")
    
    # 检查是否有权限访问
    agent = crud.agent.get(db=db, id=sdk_key.agent_id)
    if not current_user.is_admin and (agent.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    
    return sdk_key


@router.delete("/{sdk_key_id}", response_model=schemas.SDKKey)
def delete_sdk_key(
    *,
    db: Session = Depends(deps.get_db),
    sdk_key_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    删除SDK密钥
    """
    sdk_key = crud.sdk_key.get(db=db, id=sdk_key_id)
    if not sdk_key:
        raise HTTPException(status_code=404, detail="SDK密钥不存在")
    
    # 检查是否有权限删除
    agent = crud.agent.get(db=db, id=sdk_key.agent_id)
    if not current_user.is_admin and (agent.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    
    sdk_key = crud.sdk_key.remove(db=db, id=sdk_key_id)
    return sdk_key 