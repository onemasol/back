from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from jose import JWTError, jwt
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import async_session_maker
from typing import AsyncGenerator
from app.db.session import engine
from app.core.security import get_token_from_header, decode_access_token
from app.db.entity.user import User
from sqlmodel import select
from uuid import UUID  # UUID를 임포트합니다.
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# ✅ 의존성 주입 함수는 async generator로 작성해야 함
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# Bearer 토큰을 위한 새로운 스킴 객체를 생성합니다.
http_bearer_scheme = HTTPBearer(
    description="로그인 또는 토큰 교환 API로 발급받은 Access Token을 입력하세요. 'Bearer'는 자동으로 추가됩니다."
)


# ✅ 비동기 + await으로 수정된 get_current_user
async def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(http_bearer_scheme), #토큰을 헤더에서 가져오는 의존성 , 임시로 주석처리 
    session: AsyncSession = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = auth.credentials  # 토큰 문자열을 가져옵니다.
    
    try:
        payload = decode_access_token(token)
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = UUID(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    result = await session.exec(select(User).where(User.id == user_id))
    user = result.first()
    
    if user is None or user.is_deleted:
        raise credentials_exception
        
    return user

