from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from .base import BaseSchema


class MCPServerBase(BaseSchema):
    name: str
    description: Optional[str] = None
    config: Dict[str, Any]


class MCPServerCreate(MCPServerBase):
    pass


class MCPServerUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class MCPServerInDBBase(MCPServerBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: Optional[str] = None


class MCPServer(MCPServerInDBBase):
    pass


class MCPServerInDB(MCPServerInDBBase):
    pass 