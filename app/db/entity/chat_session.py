from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ChatSession(SQLModel, table=True):
    session_id: UUID = Field(primary_key=True, index=True)
    user_id: UUID = Field(index=True)
    session_title: Optional[str]
    current_task: Optional[str]
    current_node: Optional[str]
    search_retry_count: Optional[int] = 0
    metadata: Optional[dict]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active_at: Optional[datetime]