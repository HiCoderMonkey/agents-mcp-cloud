from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class MCPServerBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    port: Optional[int] = None
    api_key: Optional[str] = None
    is_active: Optional[bool] = True
    status: Optional[str] = "offline"


class MCPServerCreate(MCPServerBase):
    name: str
    address: str
    port: int


class MCPServerUpdate(MCPServerBase):
    pass


class MCPServerInDBBase(MCPServerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int

    class Config:
        orm_mode = True


class MCPServer(MCPServerInDBBase):
    pass 