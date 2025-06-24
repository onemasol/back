# app/services/integration_calendar_service.py

from typing import List, Union
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.entity.event import Event
from app.db.entity.task import Task

class IntegrationCalendarService:
    """
    Event와 Task 통합 조회를 위한 서비스
    """
    async def get_unified_items_for_user(
        self, user_id: UUID, session: AsyncSession
    ) -> List[Union[Event, Task]]:
        """
        특정 사용자의 모든 Event와 Task를 조회하여 하나의 리스트로 반환
        Event는 start_at, Task는 created_at 기준으로 최신 순으로 정렬
        Returns:
            Event와 Task 객체가 섞인 통합 리스트
        """
        # 1. 사용자의 모든 Event 조회
        event_stmt = select(Event).where(Event.user_id == str(user_id))
        # session.exec 를 session.execute 로 변경
        event_result = await session.execute(event_stmt)
        events = event_result.scalars().all()

        # 2. 사용자의 모든 Task 조회
        task_stmt = select(Task).where(Task.user_id == user_id)
        # session.exec 를 session.execute 로 변경
        task_result = await session.execute(task_stmt)
        tasks = task_result.scalars().all()
        

        # 3. 두 리스트를 하나로 병합
        combined_list: List[Union[Event, Task]] = list(events) + list(tasks)

        # 4. 정렬
        sorted_list = sorted(
            combined_list,
            key=lambda item: item.start_at if isinstance(item, Event) else item.created_at,
            reverse=True
        )

        return sorted_list