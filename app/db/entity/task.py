# app/db/entity/task.py
from sqlmodel import DateTime, SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # 명확성을 위해 별칭 사용
from sqlalchemy import String

class Task(SQLModel, table=True):

    user_id: UUID = Field(
        default_factory=uuid4, 
        sa_column=Column(PG_UUID, nullable=False, index=True, comment="사용자 ID")
    ) 
    task_id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    title: str = Field(max_length=100)
    
    description: Optional[str] = Field(
            default=None,
            sa_column=Column(String, comment="태스크 상세 설명")
        )    
    status: str = Field(default="pending", max_length=30) # 'completed', 'pending'
    
    used_agents: Optional[List[Dict[str, Any]]] = Field(default=None, sa_column=Column(JSONB))
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), comment="생성 시각")
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), comment="마지막 수정 시각")
    )