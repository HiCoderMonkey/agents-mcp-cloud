from typing import List, Dict, Any, Optional, Union, Set, Tuple

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
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[MCPServer]:
        """
        获取指定用户的所有MCP服务器
        """
        servers = (
            db.query(self.model)
            .filter(MCPServer.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return self._convert_list_ids_to_str(servers)
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[MCPServer]:
        """
        通过名称获取MCP服务器
        """
        server = db.query(self.model).filter(MCPServer.name == name).first()
        return self._convert_id_to_str(server) if server else None

    def get_multi_by_ids(
        self, 
        db: Session, 
        *, 
        ids: List[Any]
    ) -> List[MCPServer]:
        """
        通过ID列表批量获取MCP服务器
        
        Args:
            db: 数据库会话
            ids: 服务器ID列表
            
        Returns:
            List[MCPServer]: 找到的MCP服务器列表
        """
        servers = db.query(self.model).filter(self.model.id.in_(ids)).all()
        return self._convert_list_ids_to_str(servers)
    
    def validate_servers_exist_and_accessible(
        self,
        db: Session,
        *,
        server_ids: List[Any]
    ) -> Tuple[bool, Set[str], Set[str]]:
        """
        验证服务器是否存在且用户是否有权限访问
        
        Args:
            db: 数据库会话
            server_ids: 要验证的服务器ID列表
            is_admin: 是否是管理员
            
        Returns:
            Tuple[bool, Set[str]]:
            - 是否全部验证通过
            - 不存在的服务器ID集合
        """
        # 确保所有ID都是字符串类型
        server_ids = [str(id) for id in server_ids]
        
        # 查询所有指定的服务器
        servers = self.get_multi_by_ids(db, ids=server_ids)
        
        # 检查是否所有服务器都存在
        found_ids = {str(server.id) for server in servers}
        missing_ids = set(server_ids) - found_ids
        
        is_valid = len(missing_ids) == 0 
        return (is_valid, missing_ids)


mcp_server = CRUDMCPServer(MCPServer) 