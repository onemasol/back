# app/api/v1/routers/documents.py

from fastapi import APIRouter, UploadFile, File, Form, Depends
from pydantic import BaseModel
from datetime import datetime
from app.services.ocr_service import OcrService
from app.dto.document_dto import (
    ConfirmItemsRequest,
    ConfirmItemsResponse,
    ProcessImageResponse
)
from app.services.document_service import DocumentService
import uuid
from app.api.v1.deps import get_session, get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.entity.user import User
# 라우터를 생성
router = APIRouter(prefix="/documents", tags=["Documents"])

# OcrService 인스턴스를 생성
ocr_service = OcrService()

# API의 최종 응답 형식을 Pydantic 모델로 정의
class OcrProcessResponse(BaseModel):
    user_id: str
    user_message: str
    extracted_text: str

@router.post("/process-image", response_model=OcrProcessResponse, # 명확한 응답 모델 지정
    summary="이미지 처리 및 Document 생성")
async def process_image_and_data(
    # multipart/form-data 형식의 요청을 처리
    # 파일은 File()로, 다른 텍스트 데이터는 Form()으로 받기
    file: UploadFile = File(..., description="OCR 처리를 위한 이미지 파일"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    user_message: str = Form(..., description="사용자가 이미지와 함께 입력한 메시지 (맥락)"),
):
    """
    이미지 파일과 사용자 데이터를 함께 받아 OCR 처리를 수행하고,
    추출된 텍스트를 포함하여 모든 데이터를 "모델 쪽" 서버로 전달할 수 있는
    형식으로 반환
    """
    # 1. DocumentService 인스턴스를 생성합니다.
    doc_service = DocumentService(session)

    # 2. 모든 로직을 서비스에 위임합니다.
    new_doc = await doc_service.create_document_from_image(
        user=current_user,
        user_message=user_message,
        file=file
    )
    
    # 3. 서비스로부터 받은 결과로 최종 응답을 생성합니다.
    return OcrProcessResponse(
        user_id=str(current_user.id),
        user_message=new_doc.user_message,
        extracted_text=new_doc.extracted_text)

@router.post(
    "/{doc_id}/confirm",
    response_model=ConfirmItemsResponse,
    summary="추출 일정 저장 확정"
)
async def confirm_and_save_extracted_schedules(
    doc_id: uuid.UUID,
    request_body: ConfirmItemsRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> ConfirmItemsResponse:
    """
    사용자가 선택한 일정들을 실제 캘린더(Event 테이블)에 저장합니다.
    """
    await DocumentService(session).confirm_and_save_items(
        doc_id=doc_id,
        user=current_user,
        items_to_save=request_body
    )
    
    return ConfirmItemsResponse(
        message=f"요청하신 내용이 성공적으로 저장되었습니다."
    )
