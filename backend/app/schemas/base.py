from typing import Any
from pydantic import BaseModel, ConfigDict
from sqlalchemy import inspect, BigInteger


class BaseSchema(BaseModel):
    """
    所有 schema 的基类
    """
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        """
        从 ORM 对象创建 schema 实例，确保所有 BigInteger 类型的字段都转换为字符串
        """
        if obj is None:
            return None
            
        # 获取对象的 SQLAlchemy 检查器
        if hasattr(obj, '__table__'):
            inspector = inspect(obj.__class__)
            
            # 遍历所有列
            for column in inspector.columns:
                if isinstance(column.type, BigInteger):
                    value = getattr(obj, column.key, None)
                    if value is not None:
                        setattr(obj, column.key, str(value))
        
        return super().from_orm(obj)