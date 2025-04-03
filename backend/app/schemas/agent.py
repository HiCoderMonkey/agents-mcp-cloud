from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class AgentBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2048
    mcp_server_id: Optional[int] = None
    is_active: Optional[bool] = True


class AgentCreate(AgentBase):
    name: str
    user_id: int


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    mcp_server_id: Optional[int] = None
    is_active: Optional[bool] = None


class AgentInDBBase(AgentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int

    class Config:
        from_attributes = True


class Agent(AgentInDBBase):
    pass


class AgentInDB(AgentInDBBase):
    pass 