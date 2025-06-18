# app/integrations/google.py

import httpx
from fastapi import HTTPException, status
from app.core.config import settings
from app.dto.auth_dto import GoogleTokenInfo

async def verify_google_id_token(id_token: str) -> GoogleTokenInfo:
    """
    Google ID 토큰을 검증하고 사용자 정보를 담은 DTO를 반환합니다.
    불필요한 userinfo API 호출을 제거하여 효율성을 높입니다.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://oauth2.googleapis.com/tokeninfo",
                params={"id_token": id_token}
            )
            response.raise_for_status()  # 2xx 상태 코드가 아니면 예외 발생
            
            token_info_data = response.json()

            # 클라이언트 ID 검증
            if token_info_data.get("aud") != settings.GOOGLE_CLIENT_ID:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid client ID in token."
                )

            return GoogleTokenInfo(**token_info_data)

        except httpx.HTTPStatusError as e:
            # 구글 서버에서 오류 응답이 온 경우
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error verifying Google token: {e.response.text}"
            )
        except Exception as e:
            # 네트워크 오류 또는 기타 예외
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred during token verification: {str(e)}"
            )