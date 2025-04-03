from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.chat_message import ChatMessage
from app.schemas.chat_message import ChatMessageCreate, ChatMessageUpdate


class CRUDChatMessage(CRUDBase[ChatMessage, ChatMessageCreate, ChatMessageUpdate]):
    def get_by_agent(
        self, db: Session, *, agent_id: int, skip: int = 0, limit: int = 100
    ) -> List[ChatMessage]:
        return (
            db.query(self.model)
            .filter(ChatMessage.agent_id == agent_id)
            .order_by(ChatMessage.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[ChatMessage]:
        return (
            db.query(self.model)
            .filter(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_agent_and_user(
        self, db: Session, *, agent_id: int, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[ChatMessage]:
        return (
            db.query(self.model)
            .filter(ChatMessage.agent_id == agent_id, ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


chat_message = CRUDChatMessage(ChatMessage) 