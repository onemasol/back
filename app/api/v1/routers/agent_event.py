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
