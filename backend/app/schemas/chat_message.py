from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ChatMessageBase(BaseModel):
    content: str
    role: str
    agent_id: int
    session_id: Optional[str] = None
    parent_id: Optional[int] = None
    user_id: Optional[int] = None


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageUpdate(BaseModel):
    content: Optional[str] = None
    role: Optional[str] = None
    agent_id: Optional[int] = None
    session_id: Optional[str] = None
    parent_id: Optional[int] = None
    user_id: Optional[int] = None


class ChatMessageInDBBase(ChatMessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatMessage(ChatMessageInDBBase):
    pass


class ChatMessageInDB(ChatMessageInDBBase):
    pass 