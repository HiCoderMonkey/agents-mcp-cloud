from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func

from app.models.base_model import BaseModel


class MCPServer(BaseModel):
    __tablename__ = "mcp_servers"

    name = Column(String(100), nullable=False)
    description = Column(Text)
    config = Column(JSON, nullable=False, comment="MCP配置内容，JSON格式")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())