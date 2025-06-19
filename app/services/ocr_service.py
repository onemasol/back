# app/services/ocr_service.py

from fastapi import UploadFile, HTTPException
import httpx
import json
import uuid
import time
import logging

from app.core.config import settings # config 파일에서 설정을 불러옵니다.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OcrService:
    async def extract_text_from_image(self, file: UploadFile) -> str:
        """
        Naver CLOVA OCR API를 호출하여 이미지에서 텍스트를 추출
        """
        logger.info(f"Forwarding file to CLOVA OCR API: {file.filename}")
        
        request_json = {
            "images": [{"format": file.content_type.split('/')[-1], "name": "ocr_image"}],
            "requestId": str(uuid.uuid4()),
            "version": "V2",
            "timestamp": int(time.time() * 1000),
        }

        payload = {"message": json.dumps(request_json).encode("UTF-8")}
        files = [("file", (file.filename, await file.read(), file.content_type))]
        headers = {"X-OCR-SECRET": settings.CLOVA_OCR_SECRET_KEY}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.CLOVA_OCR_APIGW_URL,
                    data=payload,
                    files=files,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                
                result = response.json()
                
                # CLOVA OCR 결과에서 텍스트만 추출하여 하나의 문자열로 합칩니다.
                extracted_lines = []
                for image in result.get("images", []):
                    for field in image.get("fields", []):
                        extracted_lines.append(field.get("inferText", ""))
                
                full_text = "\n".join(extracted_lines)
                logger.info(f"Successfully received OCR result from CLOVA API for {file.filename}.")
                return full_text

        except httpx.HTTPStatusError as e:
            logger.error(f"CLOVA OCR API request failed: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"CLOVA OCR API Error: {e.response.text}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during CLOVA OCR API call: {e}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")