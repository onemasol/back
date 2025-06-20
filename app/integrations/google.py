# app/integrations/google.py

from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, status
import logging
from app.core.config import settings
from app.dto.auth_dto import GoogleTokenInfo

logger = logging.getLogger(__name__)

async def verify_google_id_token(token: str) -> GoogleTokenInfo:
    """
    Google ID 토큰을 검증하고, 여러 클라이언트 ID를 지원합니다.
    """
    try:
        # 1. 특정 client_id를 지정하지 않고, 토큰의 유효성(서명, 만료시간)만 먼저 검증
        id_info = id_token.verify_oauth2_token(
            token, requests.Request()
        )

        # 2. 토큰에서 'aud' (audience, 대상 클라이언트 ID) 값을 추출
        audience = id_info.get("aud")
        if not audience:
            raise ValueError("ID token is missing 'aud' claim.")

        # 3. .env 파일에 설정된 허용된 클라이언트 ID 목록을 불러오기
        allowed_client_ids = [
            client_id.strip() for client_id in settings.GOOGLE_ALLOWED_CLIENT_IDS.split(',')
        ]

        # 4. 토큰의 audience가 우리 서버가 허용한 목록에 있는지 직접 확인
        if audience not in allowed_client_ids:
            logger.warning(f"Unauthorized token audience: {audience}")
            raise ValueError(f"Token's audience '{audience}' is not in the allowed list.")

        # 5. 모든 검증을 통과하면, 사용자 정보를 DTO로 변환하여 반환
        return GoogleTokenInfo(**id_info)

    except ValueError as e:
        # 토큰이 유효하지 않거나, audience가 일치하지 않는 모든 경우에 에러 처리
        logger.error(f"Google token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Google token: {e}"
        )