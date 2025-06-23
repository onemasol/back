# app/dto/integration_calendar_dto.py

from typing import List, Union
from app.dto.event_dto import EventRead
from app.dto.task_dto import TaskReadDTO

# Event 또는 Task가 될 수 있는 통합 아이템 타입 정의
UnifiedItem = Union[EventRead, TaskReadDTO]

# API 응답 모델
UnifiedSearchResponse = List[UnifiedItem]