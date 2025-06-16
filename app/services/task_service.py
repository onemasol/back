# app/services/task_service.py
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime, timezone
from uuid import UUID

from app.db.entity.task import Task
from app.dto.task_dto import TaskCreateDTO, TaskReadDTO

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