# app/api/v1/routers/agent.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from app.api.v1.deps import get_session, get_current_user
from app.db.entity.user import User
from app.services.calender_service import CalendarService
from app.services.task_service import TaskService
from app.dto.task_dto import TaskCreateDTO, TaskReadDTO 
from app.dto.event_dto import EventCreateDTO, EventUpdateDTO, AgentEventCreateDTO

# 라우터 설정
router = APIRouter(prefix="/agent", tags=["Agent event"])

# 서비스 인스턴스 생성
calendar_service = CalendarService()

# --- Event API (수정된 부분) ---
@router.post("/events", summary="에이전트에 의한 Event 생성", response_model=dict)
async def create_agent_event(
    dto: AgentEventCreateDTO, # 일반 DTO가 아닌 AgentTaskCreateDTO를 사용합니다.
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    에이전트가 사용자를 위해 태스크를 생성
    `used_agents` 필드에 어떤 에이전트가 사용되었는지 정보를 포함
    """

    return await calendar_service.create_event(dto, user.id, session)

@router.get("/events/{event_id}", summary="특정 Event 조회", response_model=dict)
async def read_agent_event(
    event_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    `event_id`를 사용하여 특정 이벤트의 정보를 조회합니다.
    - 해당 이벤트가 존재하지 않거나, 현재 사용자의 이벤트가 아니면 404 에러를 반환
    """
    return await calendar_service.read_event(event_id=event_id, user_id=user.id, session=session)

@router.put("/events/{event_id}", summary="특정 Event 수정", response_model=dict)
async def update_agent_event(
    event_id: UUID,
    dto: EventUpdateDTO, # 수정을 위한 DTO
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    `event_id`를 사용하여 특정 이벤트를 수정합니다.
    - 해당 이벤트가 존재하지 않거나, 현재 사용자의 이벤트가 아니면 404 에러를 반환
    """
    return await calendar_service.update_event(event_id=event_id, dto=dto, user_id=user.id, session=session)

@router.delete("/events/{event_id}", summary="특정 Event 삭제", response_model=dict)
async def delete_agent_event(
    evnent_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    `event_id`를 사용하여 특정 이벤트를 삭제합니다.
    - 해당 이벤트가 존재하지 않거나, 현재 사용자의 이벤트가 아니면 404 에러를 반환
    """
    return await calendar_service.delete_event(event_id=evnent_id, user_id=user.id, session=session)
    