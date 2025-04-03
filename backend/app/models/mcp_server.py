from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class MCPServer(BaseModel):
    __tablename__ = "mcp_servers"

    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    api_key = Column(String(255))
    is_active = Column(Boolean, default=True)
    status = Column(String(50), default="offline")  # online, offline, error
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 外键关系
    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User", back_populates="mcp_servers")
    
    # 反向关系
    agents = relationship("Agent", back_populates="mcp_server", cascade="all, delete-orphan") 