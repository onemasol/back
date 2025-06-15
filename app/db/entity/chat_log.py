from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class ChatLog(SQLModel, table=True):
    chat_id: UUID = Field(primary_key=True, index=True)
    session_id: UUID = Field(index=True)
    user_id: UUID = Field(index=True)
    task_id: Optional[UUID]
    message: str
    role: Optional[str]
    agent_type: Optional[str]
    step_order: Optional[int]
    is_final_response: Optional[bool]
    embedding_id: Optional[UUID]
    description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
