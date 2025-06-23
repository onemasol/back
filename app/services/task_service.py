# app/services/task_service.py
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime, timezone
from uuid import UUID
from typing import List
from app.db.entity.task import Task
from app.dto.task_dto import TaskCreateDTO, TaskReadDTO, TaskUpdateDTO

class TaskService:
    async def create_task(self, dto: TaskCreateDTO, user_id: UUID, session: AsyncSession) -> TaskReadDTO:
        # Task 엔티티 생성 시 user_id를 함께 전달
        new_task = Task(**dto.model_dump(), user_id=user_id)
        
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return TaskReadDTO.from_orm(new_task)

    async def get_task(self, task_id: UUID, user_id: UUID, session: AsyncSession) -> TaskReadDTO:
        # task_id (UUID)와 user_id로 조회
        result = await session.exec(
            select(Task).where(Task.task_id == task_id, Task.user_id == user_id)
        )
        task = result.first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found or you don't have permission")
            
        return TaskReadDTO.from_orm(task)
    
    async def get_tasks_by_user(self, user_id: UUID, session: AsyncSession) -> List[Task]:
        """
        특정 사용자의 모든 태스크 목록을 DB에서 조회합니다.
        """
        result = await session.exec(select(Task).where(Task.user_id == user_id))
        return result.all()
    
    async def update_task(self, task_id: UUID, user_id: UUID, dto: TaskUpdateDTO, session: AsyncSession) -> TaskReadDTO:
        """
        ID로 태스크를 찾아 내용을 수정합니다.
        """
        result = await session.exec(
            select(Task).where(Task.task_id == task_id, Task.user_id == user_id)
        )
        task_to_update = result.first()

        if not task_to_update:
            raise HTTPException(status_code=404, detail="Task not found or you don't have permission")

        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task_to_update, key, value)

        session.add(task_to_update)
        await session.commit()
        await session.refresh(task_to_update)

        return TaskReadDTO.from_orm(task_to_update)

    async def delete_task(self, task_id: UUID, user_id: UUID, session: AsyncSession):
        """
        ID로 태스크를 찾아 삭제합니다.
        """
        result = await session.exec(
            select(Task).where(Task.task_id == task_id, Task.user_id == user_id)
        )
        task_to_delete = result.first()

        if not task_to_delete:
            raise HTTPException(status_code=404, detail="Task not found or you don't have permission")

        await session.delete(task_to_delete)
        await session.commit()
        return