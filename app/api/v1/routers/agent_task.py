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
from app.dto.task_dto import TaskCreateDTO

# 라우터 설정
router = APIRouter(prefix="/agent", tags=["Agent Task"])

# 서비스 인스턴스 생성

task_service = TaskService()


# --- 태스크 API (수정된 부분) ---

# 태스크 생성 API
@router.post("/tasks", summary="Task 생성", response_model=TaskReadDTO) 
async def agent_create_task(
    task_dto: TaskCreateDTO,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return await task_service.create_task(task_dto, user.id, session)

# 태스크 조회 API
@router.get("/tasks/{task_id}", summary="Task 조회", response_model=TaskReadDTO)
async def agent_get_task(
    task_id: UUID, # int -> UUID
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    # 서비스 호출 시 task_id (UUID) 전달
    return await task_service.get_task(task_id, user.id, session)

