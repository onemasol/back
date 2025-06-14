# filepath: d:\onemasol\app\db\entity\session.py
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
import uuid

class Session(SQLModel, table=True):
    session_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        max_length=36
    )
    user_id: str = Field(..., max_length=36)
    session_title: Optional[str] = Field(default=None, max_length=100)
    current_task: Optional[str] = Field(default=None, max_length=50)
    current_node: Optional[str] = Field(default=None, max_length=50)
    search_retry_count: Optional[int] = Field(default=0)
    metadata: Optional[dict] = Field(
        default_factory=dict,
        sa_column=Column(JSONB)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active_at: Optional[datetime] = Field(default=None)