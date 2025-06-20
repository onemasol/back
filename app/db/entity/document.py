# app/db/entity/document.py

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import Enum, Field, SQLModel, JSON, Column

from pydantic import ConfigDict

# 문서 처리 상태를 나타내기 위한 Enum (선택 사항이지만 권장)
class DocumentStatus(str, Enum):
     AWAITING_CONFIRMATION = "AWAITING_CONFIRMATION" # 사용자에게 확인 대기 중
     COMPLETED = "COMPLETED" # 사용자가 확정하여 일정 저장 완료
     FAILED = "FAILED" # 처리 실패



class Document(SQLModel, table=True):
# --- 👇 여기에 model_config를 추가! ---
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # API의 {doc_id}로 사용될 고유 ID
    doc_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID, primary_key=True, nullable=False),
    )
    user_id: uuid.UUID = Field(nullable=False)

    # 이 문서가 속한 채팅 세션의 ID
    session_id: uuid.UUID = Field(nullable=False)

    
    # 처리 상태
    status: str = Field(default="AWAITING_CONFIRMATION", index=True)
    
    # OCR을 통해 추출된 순수 텍스트
    extracted_text: Optional[str] = Field(default=None)

    # 이 OCR 작업을 유발한 사용자의 원본 메시지 (예: "이 사진에서 일정 뽑아줘")
    user_message: Optional[str] = Field(default=None)
    
    # 사용자가 메시지를 보낸 시간
    sent_at: datetime = Field(default_factory=datetime.now)

    extracted_schedules: Optional[List[Dict[str, Any]]] = Field(default=None, sa_column=Column(JSON))
    
    # 생성 및 수정 시간
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)