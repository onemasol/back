# routes/auth.py
from fastapi import APIRouter, Depends, Header
from app.api.v1.deps import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.dto.auth_dto import GoogleToken, LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/oauth/google",
            response_model=LoginResponse,
            summary="Google OAuth2.0 Login")
async def google_oauth_login(
    token_data: GoogleToken,  # Authorization 헤더 대신 body로 받음
    session: AsyncSession = Depends(get_session)
) -> LoginResponse:
    """
    Google ID Token을 받아 서버 Access Token으로 교환합니다.
    """
    auth_service = AuthService(session)
    return await auth_service.google_login(token_data.id_token)

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    summary="Refresh Access Token"
)
async def refresh_token(
    req: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session)
) -> RefreshTokenResponse:
    """
    유효한 Refresh Token을 사용하여 만료된 Access Token을 갱신합니다.
    """
    auth_service = AuthService(session)
    return await auth_service.refresh_access_token(req)