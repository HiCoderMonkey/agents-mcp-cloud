from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from .base import BaseSchema


class AgentBase(BaseSchema):
    name: str
    description: Optional[str] = None
    model: str
    temperature: float = 0.7
    max_tokens: int = 2048
    mcp_server_ids: List[str] = []
    is_active: bool = True
    instructions: Optional[str] = None
    llm_api_url: Optional[str] = Field(None, description="LLM服务接口地址")
    api_key: Optional[str] = Field(None, description="API密钥")


class AgentCreate(AgentBase):
    name: str
    user_id: str


class AgentUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    mcp_server_ids: Optional[List[str]] = None
    is_active: Optional[bool] = None
    instructions: Optional[str] = None
    llm_api_url: Optional[str] = Field(None, description="LLM服务接口地址")
    api_key: Optional[str] = Field(None, description="API密钥")


class AgentInDBBase(AgentBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: str

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.isoformat()
        }
    )

    @classmethod
    def from_orm(cls, obj):
        # 确保 id 字段被转换为字符串
        if hasattr(obj, 'id'):
            obj.id = str(obj.id)
        return super().from_orm(obj)


class Agent(AgentInDBBase):
    pass


class AgentInDB(AgentInDBBase):
    pass 