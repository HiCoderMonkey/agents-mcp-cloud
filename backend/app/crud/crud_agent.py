from typing import List, Dict, Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate


class CRUDAgent(CRUDBase[Agent, AgentCreate, AgentUpdate]):
    def create_with_user(
            self, db: Session, *, obj_in: AgentCreate, user_id: int
    ) -> Agent:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        db_obj.id = str(db_obj.id)
        return db_obj

    def get_multi_by_user(
            self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Agent]:
        items = (
            db.query(self.model)
            .filter(Agent.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        for item in items:
            item.id = str(item.id)
        return items

    def get_multi_by_mcp_server(
            self, db: Session, *, mcp_server_id: int, skip: int = 0, limit: int = 100
    ) -> List[Agent]:
        return (
            db.query(self.model)
            .filter(Agent.mcp_server_id == mcp_server_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_name(self, db: Session, *, name: str, user_id: int) -> Optional[Agent]:
        return db.query(self.model).filter(Agent.name == name, Agent.user_id == user_id).first()

    def get(self, db: Session, id: Any) -> Optional[Agent]:
        obj = super().get(db, id)
        if obj:
            obj.id = str(obj.id)
        return obj


agent = CRUDAgent(Agent)
