from typing import List, Dict, Any, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.mcp_server import MCPServer
from app.schemas.mcp_server import MCPServerCreate, MCPServerUpdate


class CRUDMCPServer(CRUDBase[MCPServer, MCPServerCreate, MCPServerUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: MCPServerCreate, user_id: int
    ) -> MCPServer:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[MCPServer]:
        return (
            db.query(self.model)
            .filter(MCPServer.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[MCPServer]:
        return db.query(self.model).filter(MCPServer.name == name).first()


mcp_server = CRUDMCPServer(MCPServer) 