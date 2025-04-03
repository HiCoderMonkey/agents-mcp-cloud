from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class AgentBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "inactive"
    instructions: Optional[str] = None
    is_active: Optional[bool] = True
    mcp_server_id: Optional[int] = None


class AgentCreate(AgentBase):
    name: str


class AgentUpdate(AgentBase):
    pass


class AgentInDBBase(AgentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int

    class Config:
        orm_mode = True


class Agent(AgentInDBBase):
    pass 