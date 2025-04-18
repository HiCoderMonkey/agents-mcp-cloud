from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class Agent(BaseModel):
    __tablename__ = "agents"

    name = Column(String(100), index=True)
    description = Column(Text, nullable=True)
    model = Column(String(50))
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=2048)
    mcp_server_ids = Column(JSON, default=list)  # 修改为JSON类型，存储MCP服务器ID列表
    status = Column(String(50), default="inactive")  # active, inactive, error
    instructions = Column(Text)
    is_active = Column(Boolean, default=True)
    user_id = Column(BigInteger, nullable=False)
    llm_api_url = Column(String(500), nullable=True)
    api_key = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    