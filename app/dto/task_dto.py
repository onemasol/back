# app/dto/task_dto.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# --- 공통 필드를 정의하는 내부용 Base 모델 ---
class _TaskBase(BaseModel):
    title: str = Field(..., max_length=100, description="태스크 이름")
    description: Optional[str] = Field(None, description="태스크 상세 설명")
    status: str = Field("pending", max_length=30, description="태스크 상태")

# --- 사용자가 직접 생성 시 사용할 DTO ---
class TaskCreateDTO(_TaskBase):
    pass

# --- 에이전트가 생성 시 사용할 DTO ---
class AgentTaskCreateDTO(_TaskBase):
    used_agents: Optional[List[Dict[str, Any]]] = Field(None, description="수행에 사용된 agent 목록")

# --- 태스크 수정 시 사용할 DTO ---
class TaskUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, max_length=100, description="태스크 이름")
    description: Optional[str] = Field(None, description="태스크 상세 설명")
    status: Optional[str] = Field(None, max_length=30, description="태스크 상태")
    used_agents: Optional[List[Dict[str, Any]]] = Field(None, description="수행에 사용된 agent 목록")

# --- 태스크 조회 시 사용할 DTO ---
class TaskReadDTO(_TaskBase):
    task_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    used_agents: Optional[List[Dict[str, Any]]] # 조회 시에는 에이전트 정보도 포함

    class Config:
        from_attributes = True # ORM 모델을 DTO로 변환 가능하게 설정