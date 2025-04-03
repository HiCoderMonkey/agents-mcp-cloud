from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.declarative import declared_attr

from app.db.session import Base
from app.utils.snowflake import id_worker


class BaseModel(Base):
    """
    所有模型的基类，提供雪花算法ID
    """
    __abstract__ = True  # 声明为抽象类，不会创建实际的表
    
    # 使用雪花算法生成ID
    id = Column(BigInteger, primary_key=True, index=True)
    
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