from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class SDKKey(BaseModel):
    __tablename__ = "sdk_keys"

    key = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    user_id = Column(BigInteger, nullable=False)
    agent_id = Column(BigInteger, nullable=False)