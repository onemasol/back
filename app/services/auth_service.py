# app/services/auth_service.py

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.entity.user import User
from app.dto.auth_dto import GoogleTokenInfo, LoginResponse
from app.integrations import google
from app.core.security import create_access_token


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_or_create_user(self, token_info: GoogleTokenInfo) -> User:
        """
        Google 정보 기반으로 사용자를 조회하거나 새로 생성합니다.
        """
        # 1. google_user_id (sub) 기준으로 사용자 조회
        query = select(User).where(User.google_user_id == token_info.sub)
        result = await self.session.exec(query)
        user = result.first()

        if user:
            # 기존 유저 정보 업데이트 (선택적)
            user.name = token_info.name
        else:
            # 2. 사용자가 없으면 이메일로 다시 조회 (기존에 다른 방식으로 가입했을 경우 대비)
            query = select(User).where(User.email == token_info.email)
            result = await self.session.exec(query)
            user = result.first()
            if user:
                # 이메일이 같은 기존 사용자가 있으면 google_user_id 업데이트
                user.google_user_id = token_info.sub
                user.name = token_info.name
                user.profile_image_url = token_info.picture
            else:
                # 3. 완전히 새로운 사용자 생성
                user = User(
                    google_user_id=token_info.sub,
                    email=token_info.email,
                    name=token_info.name,
                    profile_image_url=token_info.picture
                )
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def google_login(self, id_token: str) -> LoginResponse:
        """
        Google ID 토큰을 사용하여 로그인/회원가입을 처리하고 내부 JWT를 발급합니다.
        """
        # 1. 구글 ID 토큰 검증 및 사용자 정보 가져오기
        token_info = await google.verify_google_id_token(id_token)

        # 2. 사용자 정보로 DB에서 유저 조회 또는 생성
        user = await self._get_or_create_user(token_info)

        # 3. 내부 서비스용 Access Token 생성
        access_token = create_access_token(subject=str(user.id))
        
        return LoginResponse(access_token=access_token)