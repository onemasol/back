from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ChatTransactionLog(BaseModel):
    session_id: UUID
    user_id: UUID
    user_message: str
    agent_response: str
    agent_type: str
    task_id: Optional[UUID] = None
    embedding_id: Optional[UUID] = None
