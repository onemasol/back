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
from app.services.ocr_service import OcrService
from datetime import datetime
from fastapi import UploadFile
class DocumentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.ocr_service=OcrService()  # OcrService 인스턴스 생성


    async def create_document_from_image(
        self,
        user: User,
        session_id: uuid.UUID,
        user_message: str,
        sent_at: datetime,
        file: UploadFile
    ) -> Document:
        """
        라우터로부터 받은 데이터를 사용하여 OCR을 수행하고,
        그 결과를 Document 테이블에 저장합니다.
        """
        # 1. OcrService를 호출하여 이미지에서 텍스트를 추출합니다.
        extracted_text = await self.ocr_service.extract_text_from_image(file)

        # 2. //TODO 추출된 텍스트로 AI 분석을 수행결과를 저장
        # 지금은 임시로 빈 리스트를 사용합니다.
        extracted_schedules = []

        sent_at_naive = sent_at.replace(tzinfo=None)
        # 3. 모든 정보를 취합하여 Document 객체를 생성하고 DB에 저장합니다.
        new_document = Document(
            user_id=user.id,
            session_id=session_id,
            status="AWAITING_CONFIRMATION",  # AI 분석 후 사용자 확인 대기 상태
            extracted_text=extracted_text,
            user_message=user_message,
            sent_at=sent_at_naive,
            extracted_schedules=extracted_schedules
        )

        self.session.add(new_document)
        await self.session.commit()
        await self.session.refresh(new_document)

        return new_document

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
        
        calendar_service = CalendarService()
        task_service = TaskService()

        for item in items_to_save.items:
            if item.type == "event":
                event_data: EventCreateDTO = item.data
                
                # CalendarService.create_event의 시그니처에 맞춰 인자를 전달합니다.
                await calendar_service.create_event(
                    event=event_data, 
                    user_id=user.id, 
                    session=self.session
                )

            elif item.type == "task":
                task_data: TaskCreateDTO = item.data

                # TaskService.create_task의 시그니처에 맞춰 인자를 전달합니다.
                await task_service.create_task(
                    dto=task_data, 
                    user_id=user.id, 
                    session=self.session
                )
        
        # --- 3. 문서 상태 업데이트 로직---
        query = select(Document).where(Document.doc_id == doc_id, Document.user_id == user.id)
        result = await self.session.exec(query)
        doc_to_update = result.one_or_none()
        
        if doc_to_update:
            doc_to_update.status = "COMPLETED"
            self.session.add(doc_to_update)
            await self.session.commit()
        
        return
    

