from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.sdk_key import SDKKey
from app.schemas.sdk_key import SDKKeyCreate, SDKKeyUpdate


class CRUDSDKKey(CRUDBase[SDKKey, SDKKeyCreate, SDKKeyUpdate]):
    def create_with_key(
        self, db: Session, *, obj_in: SDKKeyCreate, key: str, expires_at: datetime = None
    ) -> SDKKey:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, key=key, expires_at=expires_at)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_agent(
        self, db: Session, *, agent_id: int, skip: int = 0, limit: int = 100
    ) -> List[SDKKey]:
        return (
            db.query(self.model)
            .filter(SDKKey.agent_id == agent_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[SDKKey]:
        return (
            db.query(self.model)
            .join(SDKKey.agent)
            .filter(SDKKey.agent.has(user_id=user_id))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_key(self, db: Session, *, key: str) -> Optional[SDKKey]:
        return db.query(self.model).filter(SDKKey.key == key).first()
    
    def is_key_valid(self, db: Session, *, key: str) -> bool:
        """检查SDK密钥是否有效（存在、激活状态、未过期）"""
        sdk_key = self.get_by_key(db, key=key)
        if not sdk_key:
            return False
        if not sdk_key.is_active:
            return False
        if sdk_key.expires_at and sdk_key.expires_at < datetime.utcnow():
            return False
        return True


sdk_key = CRUDSDKKey(SDKKey) 