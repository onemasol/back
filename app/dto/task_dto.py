# app/dto/task_dto.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class TaskBase(BaseModel):
    title: Optional[str] = Field(..., max_length=100, description="태스크 이름")
    description: Optional[str] = Field(None, description="태스크 상세 설명")
    status: str = Field("pending", max_length=30, description="태스크 상태")
    used_agents: Optional[List[Dict[str, Any]]] = Field(None, description="수행에 사용된 agent 목록")

class TaskCreateDTO(TaskBase):
    pass

class TaskReadDTO(TaskBase):
    task_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # ORM 모델을 DTO로 변환 가능하게 설정