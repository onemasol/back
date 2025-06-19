# app/api/v1/routers/documents.py

from fastapi import APIRouter, UploadFile, File, Form, Depends
from pydantic import BaseModel
from datetime import datetime
from app.services.ocr_service import OcrService

# 라우터를 생성
router = APIRouter(prefix="/documents", tags=["Documents"])

# OcrService 인스턴스를 생성
ocr_service = OcrService()

# API의 최종 응답 형식을 Pydantic 모델로 정의
class OcrProcessResponse(BaseModel):
    user_id: str
    user_message: str
    sent_at: datetime
    extracted_text: str
    session_id: str  

@router.post("/process-image", response_model=OcrProcessResponse)
async def process_image_and_data(
    # multipart/form-data 형식의 요청을 처리
    # 파일은 File()로, 다른 텍스트 데이터는 Form()으로 받기
    file: UploadFile = File(..., description="OCR 처리를 위한 이미지 파일"),
    user_id: str = Form(..., description="요청을 보낸 사용자의 ID"),
    session_id: str = Form(..., description="현재 채팅 세션의 ID"),
    user_message: str = Form(..., description="사용자가 이미지와 함께 입력한 메시지 (맥락)"),
    sent_at: datetime = Form(..., description="프론트엔드에서 요청을 보낸 시각 (ISO 8601 형식)")
):
    """
    이미지 파일과 사용자 데이터를 함께 받아 OCR 처리를 수행하고,
    추출된 텍스트를 포함하여 모든 데이터를 "모델 쪽" 서버로 전달할 수 있는
    형식으로 반환
    """
    # 1. OcrService를 호출하여 이미지에서 텍스트를 추출
    # UploadFile 객체를 OcrService의 메서드에 전달하여 OCR 처리
    extracted_text = await ocr_service.extract_text_from_image(file)
    
    # 2. 응답 객체 생성
    response_data = OcrProcessResponse(
        user_id=user_id,
        user_message=user_message,
        sent_at=sent_at,
        extracted_text=extracted_text,
        session_id=session_id
    )
    
    # 3. 생성된 응답 객체를 반환
    return response_data