# app/api/v1/routers/tasks.py

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from typing import List

from app.api.v1.deps import get_session, get_current_user
from app.db.entity.user import User
from app.dto.task_dto import TaskCreateDTO, TaskReadDTO, TaskUpdateDTO
from app.services.task_service import TaskService

# 사용자가 직접 Task를 관리하는 새로운 라우터를 생성합니다.
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# 서비스 인스턴스 생성
task_service = TaskService()


@router.post("", response_model=TaskReadDTO, status_code=201, summary="새로운 태스크 생성 (사용자 직접)")
async def create_task(
    dto: TaskCreateDTO, # 에이전트 필드가 없는 일반 생성 DTO를 사용
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    사용자가 직접 태스크를 생성합니다. `used_agents` 필드는 자동으로 `None`으로 처리됩니다.
    """
    # 서비스의 create_task 메소드는 이 DTO를 받아 올바르게 처리합니다.
    return await task_service.create_task(dto, current_user.id, session)


@router.get("", response_model=List[TaskReadDTO], summary="사용자의 모든 태스크 목록 조회")
async def get_all_tasks(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    로그인된 사용자의 모든 태스크 목록을 조회합니다.
    """
    tasks_orm = await task_service.get_tasks_by_user(current_user.id, session)
    # 서비스로부터 받은 ORM 객체 리스트를 DTO 리스트로 변환하여 반환합니다.
    return [TaskReadDTO.from_orm(t) for t in tasks_orm]


@router.get("/{task_id}", response_model=TaskReadDTO, summary="특정 태스크 조회")
async def get_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    ID로 특정 태스크를 조회합니다.
    """
    return await task_service.get_task(task_id, current_user.id, session)


@router.put("/{task_id}", response_model=TaskReadDTO, summary="특정 태스크 수정")
async def update_task(
    task_id: UUID,
    dto: TaskUpdateDTO,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    ID로 특정 태스크를 찾아 내용을 수정합니다. 부분적인 수정도 가능합니다.
    """
    return await task_service.update_task(task_id, current_user.id, dto, session)


@router.delete("/{task_id}", status_code=204, summary="특정 태스크 삭제")
async def delete_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    ID로 특정 태스크를 삭제합니다.
    """
    await task_service.delete_task(task_id, current_user.id, session)
    # 성공적으로 삭제 시 204 No Content 응답 (본문 없음)
    return