from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD对象，默认方法使用给定的SQLAlchemy模型类型进行操作
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        return self._convert_id_to_str(obj) if obj else None

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        objs = db.query(self.model).offset(skip).limit(limit).all()
        return self._convert_list_ids_to_str(objs)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self._convert_id_to_str(db_obj)

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self._convert_id_to_str(db_obj)

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return self._convert_id_to_str(obj)

    def _convert_id_to_str(self, obj: Any) -> Any:
        """将对象的 ID 转换为字符串"""
        if hasattr(obj, 'id'):
            obj.id = str(obj.id)
        if hasattr(obj, 'user_id'):
            obj.user_id = str(obj.user_id)
        return obj

    def _convert_list_ids_to_str(self, objs: List[Any]) -> List[Any]:
        """将列表中所有对象的 ID 转换为字符串"""
        return [self._convert_id_to_str(obj) for obj in objs] 