# app/api/v1/routers/agent.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.api.v1.deps import get_session, get_current_user
from app.db.entity.user import User

# 서비스 임포트
from app.services.calender_service import CalendarService
from app.services.task_service import TaskService
from app.dto.task_dto import TaskCreateDTO, TaskReadDTO 

# DTO 임포트
from app.dto.event_dto import EventCreateDTO, EventUpdateDTO
from app.dto.task_dto import AgentTaskCreateDTO, TaskReadDTO

# 라우터 설정
router = APIRouter(prefix="/agent", tags=["Agent Task"])

# 서비스 인스턴스 생성

task_service = TaskService()


# --- 태스크 API (수정된 부분) ---

@router.post("/tasks", summary="에이전트에 의한 Task 생성", response_model=TaskReadDTO)
async def create_agent_task(
    dto: AgentTaskCreateDTO, # 일반 DTO가 아닌 AgentTaskCreateDTO를 사용합니다.
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    에이전트가 사용자를 위해 태스크를 생성합니다.
    `used_agents` 필드에 어떤 에이전트가 사용되었는지 정보를 포함
    """

    return await task_service.create_task(dto, user.id, session)

# 태스크 조회 API
@router.get("/tasks/{task_id}", summary="Task 조회", response_model=TaskReadDTO)
async def agent_get_task(
    task_id: UUID, # int -> UUID
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    # 서비스 호출 시 task_id (UUID) 전달
    return await task_service.get_task(task_id, user.id, session)

