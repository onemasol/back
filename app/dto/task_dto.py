# app/dto/task_dto.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# --- 공통 필드를 정의하는 내부용 Base 모델 ---
class _TaskBase(BaseModel):
    title: str = Field(..., max_length=100, description="태스크 이름")
    description: Optional[str] = Field(None, description="태스크 상세 설명")
    status: str = Field("pending", max_length=30, description="태스크 상태")
    due_at: Optional[datetime] = Field(None, description="마감일 (분, 초는 무시됩니다)")

# --- 사용자가 직접 생성 시 사용할 DTO ---
class TaskCreateDTO(_TaskBase):
    @field_validator('due_at', mode='before')
    @classmethod
    def truncate_to_hour(cls, v: Any) -> Optional[datetime]:
        """입력된 datetime의 분, 초, 마이크로초를 0으로 만듭니다."""
        if isinstance(v, datetime):
            return v.replace(minute=0, second=0, microsecond=0)
        # datetime이 아닌 다른 타입(예: str)으로 들어올 경우 Pydantic이 파싱하도록 그대로 반환
        return v

# --- 에이전트가 생성 시 사용할 DTO ---
class AgentTaskCreateDTO(_TaskBase):
    used_agents: Optional[List[Dict[str, Any]]] = Field(None, description="수행에 사용된 agent 목록")

    @field_validator('due_at', mode='before')
    @classmethod
    def truncate_to_hour(cls, v: Any) -> Optional[datetime]:
        """입력된 datetime의 분, 초, 마이크로초를 0으로 만듭니다."""
        if isinstance(v, datetime):
            return v.replace(minute=0, second=0, microsecond=0)
        return v

# --- 태스크 수정 시 사용할 DTO ---
class TaskUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, max_length=100, description="태스크 이름")
    description: Optional[str] = Field(None, description="태스크 상세 설명")
    status: Optional[str] = Field(None, max_length=30, description="태스크 상태")
    used_agents: Optional[List[Dict[str, Any]]] = Field(None, description="수행에 사용된 agent 목록")
    due_at: Optional[datetime] = Field(None, description="마감일 (분, 초는 무시됩니다)")

    @field_validator('due_at', mode='before')
    @classmethod
    def truncate_to_hour(cls, v: Any) -> Optional[datetime]:
        """입력된 datetime의 분, 초, 마이크로초를 0으로 만듭니다."""
        if isinstance(v, datetime):
            return v.replace(minute=0, second=0, microsecond=0)
        return v

# --- 태스크 조회 시 사용할 DTO ---
# 여기에는 유효성 검사기가 적용되지 않습니다.
class TaskReadDTO(_TaskBase):
    task_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    used_agents: Optional[List[Dict[str, Any]]] = Field(None, description="수행에 사용된 agent 목록")

    class Config:
        from_attributes = True # ORM 모델을 DTO로 변환 가능하게 설정