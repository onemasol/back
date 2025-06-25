# app/api/v1/routers/agent.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID


from app.api.v1.deps import get_session, get_current_user
from app.db.entity.user import User

# 서비스 임포트
from app.services.calender_service import CalendarService
from app.services.task_service import TaskService
from app.dto.task_dto import TaskCreateDTO, TaskReadDTO, TaskUpdateDTO 

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


@router.get("/tasks/{task_id}", summary="특정 Task 조회", response_model=TaskReadDTO)
async def read_agent_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    `task_id`를 사용하여 특정 태스크의 정보를 조회합니다.
    - 해당 태스크가 존재하지 않거나, 현재 사용자의 태스크가 아니면 404 에러를 반환
    """
    return await task_service.get_task(task_id=task_id, user_id=user.id, session=session)


@router.put("/tasks/{task_id}", summary="특정 Task 수정", response_model=TaskReadDTO)
async def update_agent_task(
    task_id: UUID,
    dto: TaskUpdateDTO, # 수정을 위한 DTO
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    `task_id`를 사용하여 특정 태스크의 정보를 수정
    - 태스크가 존재하지 않으면 404 에러를 반환
    - **dto**: 수정할 필드와 값을 담은 정보
    """
    return await task_service.update_task(task_id=task_id, dto=dto, user_id=user.id, session=session)


@router.delete("/tasks/{task_id}", summary="특정 Task 삭제")
async def delete_agent_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    `task_id`를 사용하여 특정 태스크를 삭제
    - 태스크가 존재하지 않으면 404 에러를 반환
    - 성공적으로 삭제되면 204 No Content 상태 코드를 반환
    """
    # 서비스의 삭제 메소드를 호출합니다.
    await task_service.delete_task(task_id=task_id, user_id=user.id, session=session)
    
    # 성공 시에는 아무런 본문을 반환하지 않습니다.
    return {"detail": "Task deleted successfully"}