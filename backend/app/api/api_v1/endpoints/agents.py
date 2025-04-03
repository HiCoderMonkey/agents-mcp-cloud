from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Agent])
def read_agents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取Agent列表
    """
    if current_user.is_admin:
        agents = crud.agent.get_multi(db, skip=skip, limit=limit)
    else:
        agents = crud.agent.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return agents


@router.post("/", response_model=schemas.Agent)
def create_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_in: schemas.AgentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新的Agent
    """
    # 检查MCP服务器是否存在
    if agent_in.mcp_server_id:
        mcp_server = crud.mcp_server.get(db=db, id=agent_in.mcp_server_id)
        if not mcp_server:
            raise HTTPException(status_code=404, detail="MCP服务器不存在")
        if not current_user.is_admin and mcp_server.user_id != current_user.id:
            raise HTTPException(status_code=400, detail="没有操作该MCP服务器的权限")
    
    agent = crud.agent.create_with_user(
        db=db, obj_in=agent_in, user_id=current_user.id
    )
    return agent


@router.get("/{agent_id}", response_model=schemas.Agent)
def read_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过ID获取Agent
    """
    agent = crud.agent.get(db=db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent不存在")
    if not current_user.is_admin and (agent.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    return agent


@router.put("/{agent_id}", response_model=schemas.Agent)
def update_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    agent_in: schemas.AgentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新Agent
    """
    agent = crud.agent.get(db=db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent不存在")
    if not current_user.is_admin and (agent.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    
    # 检查MCP服务器是否存在
    if agent_in.mcp_server_id:
        mcp_server = crud.mcp_server.get(db=db, id=agent_in.mcp_server_id)
        if not mcp_server:
            raise HTTPException(status_code=404, detail="MCP服务器不存在")
        if not current_user.is_admin and mcp_server.user_id != current_user.id:
            raise HTTPException(status_code=400, detail="没有操作该MCP服务器的权限")
    
    agent = crud.agent.update(
        db=db, db_obj=agent, obj_in=agent_in
    )
    return agent


@router.delete("/{agent_id}", response_model=schemas.Agent)
def delete_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    删除Agent
    """
    agent = crud.agent.get(db=db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent不存在")
    if not current_user.is_admin and (agent.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    agent = crud.agent.remove(db=db, id=agent_id)
    return agent 