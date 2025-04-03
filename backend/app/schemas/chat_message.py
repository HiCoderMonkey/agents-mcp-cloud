from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ChatMessageBase(BaseModel):
    role: str  # user, assistant
    content: str
    agent_id: int
    user_id: int


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageInDBBase(ChatMessageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ChatMessage(ChatMessageInDBBase):
    pass 