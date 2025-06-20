# app/services/document_service.py

import uuid
from typing import List, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.entity.user import User
from app.db.entity.document import Document
from app.dto.document_dto import ConfirmItemsRequest, ExtractedItem
from app.services.calender_service import CalendarService
from app.services.task_service import TaskService
from app.dto.event_dto import EventCreateDTO
from app.dto.task_dto import TaskCreateDTO

class DocumentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_document_status(self, doc_id: uuid.UUID, user_id: uuid.UUID) -> str:
        """
        문서 처리 상태를 DB에서 조회하여 반환합니다.
        """
        query = select(Document.status).where(Document.id == doc_id, Document.user_id == user_id)
        result = await self.session.exec(query)
        status = result.one_or_none()
        if not status:
            # 예외 처리: 문서가 존재하지 않는 경우
            pass
        return status

    async def get_extracted_items(self, doc_id: uuid.UUID, user_id: uuid.UUID) -> List[ExtractedItem]:
        """
        추출된 항목(일정/할일) 목록을 DB에서 조회하여 반환합니다.
        """
        query = select(Document.extracted_schedules).where(Document.id == doc_id, Document.user_id == user_id)
        result = await self.session.exec(query)
        schedules_json = result.one_or_none()
        
        # 실제로는 JSON을 ExtractedItem DTO 리스트로 변환하는 로직이 필요합니다.
        # 예시: return [ExtractedItem(**item) for item in schedules_json]
        return schedules_json or []

    async def confirm_and_save_items(
        self, doc_id: uuid.UUID, user: User, items_to_save: ConfirmItemsRequest
    ) -> None:
        """
        요청받은 items 리스트를 순회하며, 각 항목의 type에 따라
        Event 또는 Task로 분기하여 각 서비스에 저장을 위임합니다.
        """
        calendar_service = CalendarService(self.session)
        task_service = TaskService(self.session)

        # 1. 단일 'items' 리스트를 순회
        for item in items_to_save.items:
            # 2. 'type' 필드를 기준으로 분기합니다.
            if item.type == "event":
                # item.data는 이제 EventCreateDTO 타입입니다.
                event_data: EventCreateDTO = item.data
                event_data.user_id = str(user.id)
                await calendar_service.create_event(event_data)

            elif item.type == "task":
                # item.data는 이제 TaskCreateDTO 타입입니다.
                task_data: TaskCreateDTO = item.data
                await task_service.create_task(task_data, user_id=user.id)
        
        # --- 3. 문서 상태 업데이트 로직 (이전과 동일) ---
        query = select(Document).where(Document.id == doc_id, Document.user_id == user.id)
        result = await self.session.exec(query)
        doc_to_update = result.one_or_none()
        
        if doc_to_update:
            doc_to_update.status = "COMPLETED"
            self.session.add(doc_to_update)
            await self.session.commit()
        
        return