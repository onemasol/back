# app/dto/document_dto.py

import uuid
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union, Literal

# 실제 프로젝트의 DTO 클래스들을 정확하게 가져옵니다.
from app.dto.event_dto import EventCreateDTO
from app.dto.task_dto import TaskCreateDTO


# --- process-image API를 위한 응답 DTO ---
class ProcessImageResponse(BaseModel):
    """
    POST /process-image API의 응답 모델
    """
    doc_id: uuid.UUID
    status: str
    message: str = "문서 처리가 시작되었습니다. 상태를 확인해주세요."



class DocumentStatusResponse(BaseModel):
    """
    GET /status API의 응답 모델
    """
    doc_id: uuid.UUID
    status: str

class ExtractedItem(BaseModel):
    """
    GET /extracted API에서 사용할, AI가 추출한 항목 1개의 모델
    """
    type: str  # "event" 또는 "task"
    content: Dict[str, Any]

class ExtractedItemsResponse(BaseModel):
    """
    GET /extracted API의 응답 모델
    """
    items: List[ExtractedItem]

class ConfirmItem(BaseModel):
    type: Literal["event", "task"]
    data: Union[EventCreateDTO, TaskCreateDTO]

class ConfirmItemsRequest(BaseModel):
    items: List[ConfirmItem]

class ConfirmItemsResponse(BaseModel):
    """
    POST /confirm API의 응답 모델
    """
    message: str
