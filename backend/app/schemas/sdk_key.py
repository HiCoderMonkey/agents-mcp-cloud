from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class SDKKeyBase(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = True
    agent_id: int


class SDKKeyCreate(SDKKeyBase):
    pass


class SDKKeyInDBBase(SDKKeyBase):
    id: int
    key: str
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class SDKKey(SDKKeyInDBBase):
    pass 