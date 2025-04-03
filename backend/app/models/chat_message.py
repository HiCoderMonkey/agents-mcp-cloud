from sqlalchemy import Column, String, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class ChatMessage(BaseModel):
    __tablename__ = "chat_messages"

    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 外键关系
    agent_id = Column(BigInteger, ForeignKey("agents.id"))
    agent = relationship("Agent", back_populates="chat_messages")
    
    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User") 