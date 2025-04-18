from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.MCPServer])
def read_mcp_servers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取MCP服务器列表
    """
    mcp_servers = crud.mcp_server.get_multi(db, skip=skip, limit=limit)
    return mcp_servers


@router.post("/", response_model=schemas.MCPServer)
def create_mcp_server(
    *,
    db: Session = Depends(deps.get_db),
    mcp_server_in: schemas.MCPServerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新的MCP服务器
    """
    mcp_server = crud.mcp_server.create_with_user(
        db=db, obj_in=mcp_server_in, user_id=current_user.id
    )
    return mcp_server


@router.get("/{mcp_server_id}", response_model=schemas.MCPServer)
def read_mcp_server(
    *,
    db: Session = Depends(deps.get_db),
    mcp_server_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过ID获取MCP服务器
    """
    mcp_server = crud.mcp_server.get(db=db, id=mcp_server_id)
    if not mcp_server:
        raise HTTPException(status_code=404, detail="MCP服务器不存在")
    if not current_user.is_admin and (mcp_server.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    return mcp_server


@router.put("/{mcp_server_id}", response_model=schemas.MCPServer)
def update_mcp_server(
    *,
    db: Session = Depends(deps.get_db),
    mcp_server_id: int,
    mcp_server_in: schemas.MCPServerUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新MCP服务器
    """
    mcp_server = crud.mcp_server.get(db=db, id=mcp_server_id)
    if not mcp_server:
        raise HTTPException(status_code=404, detail="MCP服务器不存在")
    if not current_user.is_admin and (mcp_server.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    mcp_server = crud.mcp_server.update(
        db=db, db_obj=mcp_server, obj_in=mcp_server_in
    )
    return mcp_server


@router.delete("/{mcp_server_id}", response_model=schemas.MCPServer)
def delete_mcp_server(
    *,
    db: Session = Depends(deps.get_db),
    mcp_server_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    删除MCP服务器
    """
    mcp_server = crud.mcp_server.get(db=db, id=mcp_server_id)
    if not mcp_server:
        raise HTTPException(status_code=404, detail="MCP服务器不存在")
    if not current_user.is_admin and (mcp_server.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    mcp_server = crud.mcp_server.remove(db=db, id=mcp_server_id)
    return mcp_server 