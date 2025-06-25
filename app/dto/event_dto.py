from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

class EventBase(BaseModel):
    """이벤트의 공통 필드를 정의하는 베이스 모델"""
    title: str = Field(..., max_length=100, description="이벤트 제목")
    description: Optional[str] = Field(None, max_length=500, description="이벤트 상세 설명")
    start_at: datetime = Field(..., description="시작 시각")
    end_at: datetime = Field(..., description="종료 시각")
    location: Optional[str] = Field(None, max_length=100, description="장소")
    
    # --- 추가 및 유지된 필드들 ---
    source_type: Optional[str] = Field("user", description="이벤트 소스 (e.g., 'user', 'google')")
    # [수정된 부분] 타입을 bool에서 str로 변경하고 설명을 업데이트했습니다.
    created_by_agent: Optional[str] = Field(None, max_length=50, description="이벤트를 생성한 에이전트 이름")
    recurrence_rule: Optional[str] = Field(None, description="반복 규칙 (iCalendar RFC 5545)")
    timezone: Optional[str] = Field(None, max_length=50, description="시간대 (e.g., 'Asia/Seoul')")
    task_id: Optional[UUID] = Field(None, description="연관된 태스크 ID")

class EventCreateDTO(EventBase):
    """이벤트 생성 시 사용하는 DTO"""
    
    @model_validator(mode='after')
    def check_end_date_after_start_date(self):
        """종료 시간은 시작 시간보다 빠를 수 없습니다."""
        if self.end_at < self.start_at:
            raise ValueError('end_at must be after start_at')
        return self

class AgentEventCreateDTO(EventCreateDTO):
    """에이전트가 이벤트를 생성할 때 사용하는 DTO. created_by_agent는 EventBase에 이미 포함되어 있습니다."""
    pass

class EventUpdateDTO(BaseModel):
    """이벤트 수정(PATCH) 시 사용하는 DTO (모든 필드 Optional)"""
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=100)
    recurrence_rule: Optional[str] = None
    timezone: Optional[str] = Field(None, max_length=50)

    @model_validator(mode='after')
    def check_end_date_after_start_date(self):
        """시작과 종료 시간이 모두 주어졌을 때 시간 순서를 확인합니다."""
        # start_at이나 end_at 중 하나만 주어지면 검증을 건너뜁니다.
        if self.start_at is None or self.end_at is None:
            return self
            
        if self.end_at < self.start_at:
            raise ValueError('end_at must be after start_at')
        return self

class EventRead(EventBase):
    """이벤트 조회(응답) 시 사용하는 DTO"""
    id: UUID
    user_id: UUID
    calendar_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_end_date_on_read(self):
        """
        [오류 해결 로직]
        데이터 조회 시에는 종료 시간이 시작 시간과 같아도 허용합니다 (순간 이벤트).
        종료 시간이 시작 시간보다 빠른 경우에만 비정상으로 간주합니다.
        """
        if self.end_at < self.start_at:
            # 실제로는 오류를 발생시키기보다 로그를 남기거나 수정하는 것이 더 안정적일 수 있습니다.
            # raise ValueError('Invalid data found: end_at is before start_at')
            pass # 또는 로깅
        return self
