from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ChatTransactionLog(BaseModel):
    session_id: UUID
    user_message: str
    task_id: Optional[UUID] = None
    event_id: Optional[UUID] = None
    agent_response: str
