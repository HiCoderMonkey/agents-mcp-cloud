from sqlalchemy import Column, String, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class ChatMessage(BaseModel):
    __tablename__ = "chat_messages"

    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    agent_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
