from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class Agent(BaseModel):
    __tablename__ = "agents"

    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="inactive")  # active, inactive, error
    instructions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 外键关系
    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User", back_populates="agents")
    
    mcp_server_id = Column(BigInteger, ForeignKey("mcp_servers.id"), nullable=True)
    mcp_server = relationship("MCPServer", back_populates="agents")
    
    # 反向关系
    sdk_keys = relationship("SDKKey", back_populates="agent", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="agent", cascade="all, delete-orphan") 