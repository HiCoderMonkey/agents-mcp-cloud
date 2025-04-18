from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from .base import BaseSchema


class SDKKeyBase(BaseSchema):
    name: Optional[str] = None
    is_active: bool = True
    agent_id: str


class SDKKeyCreate(SDKKeyBase):
    pass


class SDKKeyUpdate(BaseSchema):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class SDKKeyInDBBase(SDKKeyBase):
    id: str
    key: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    user_id: str


class SDKKey(SDKKeyInDBBase):
    pass


class SDKKeyInDB(SDKKeyInDBBase):
    pass 