# app/api/v1/routers/search.py

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.deps import get_session, get_current_user
from app.db.entity.user import User
from app.db.entity.event import Event
from app.db.entity.task import Task
from app.dto.event_dto import EventRead
from app.dto.task_dto import TaskReadDTO
from app.dto.integration_calendar_dto import UnifiedSearchResponse
from app.services.integration_calendar_service import IntegrationCalendarService
from uuid import UUID
router = APIRouter(prefix="/calendar", tags=["Calendar Integration"])
# 통합 조회 API

@router.get(
    "/{user_id}/all",
    response_model=UnifiedSearchResponse,
    summary="통합 조회 (Events & Tasks)"
)
async def get_all_items(
    user_id: UUID,
    #current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> UnifiedSearchResponse:
    """
    로그인한 사용자의 모든 **Event**와 **Task**를 조회하여
    하나의 리스트로 통합하여 반환
    """
    # 인스턴스화하는 클래스명을 변경합니다.
    integration_service = IntegrationCalendarService()
    
    # 서비스 로직을 호출합니다.
    orm_items = await integration_service.get_unified_items_for_user(
        user_id=user_id,
        #user_id=current_user.id,
        session=session
    )

    # ORM 객체를 각각의 DTO로 변환
    response_items: UnifiedSearchResponse = []
    for item in orm_items:
        if isinstance(item, Event):
            response_items.append(EventRead.from_orm(item)) 
        elif isinstance(item, Task):
            response_items.append(TaskReadDTO.from_orm(item))

    return response_items