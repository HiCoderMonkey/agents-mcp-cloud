from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from app.db.session import Base
from app.utils.snowflake import id_worker


class BaseModel(Base):
    """
    所有模型的基类，提供自增ID
    """
    __abstract__ = True  # 声明为抽象类，不会创建实际的表
    
    # 使用自增ID
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    
    # 自动生成表名
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    def to_dict(self):
        """
        将模型转换为字典，确保所有 BigInteger 类型的字段都转换为字符串
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # 检查字段类型是否为 BigInteger
            if value is not None and isinstance(column.type, BigInteger):
                result[column.name] = str(value)
            else:
                result[column.name] = value
        return result
    
    @classmethod
    def __declare_last__(cls):
        """
        在所有映射器设置完成后调用
        """
        # 注册事件监听器，在实例插入前设置雪花算法ID
        from sqlalchemy import event
        event.listen(cls, 'before_insert', cls._set_snowflake_id)
    
    @staticmethod
    def _set_snowflake_id(mapper, connection, target):
        """
        在实例插入前设置雪花算法ID
        """
        if target.id is None:
            target.id = id_worker.next_id() 