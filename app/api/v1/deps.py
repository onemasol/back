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
from uuid import uuid4 # 임시로 uuid4 사용

# ✅ 의존성 주입 함수는 async generator로 작성해야 함
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# ✅ 비동기 + await으로 수정된 get_current_user
async def get_current_user(
    #token: str = Depends(get_token_from_header), // 토큰을 헤더에서 가져오는 의존성 , 임시로 주석처리 
    session: AsyncSession = Depends(get_session)
) -> User:
    # try:
    #     payload = decode_access_token(token)
    #     user_id = int(payload.get("sub"))
    # except (JWTError, ValueError):
    #     raise HTTPException(status_code=401, detail="Invalid authentication")

    # result = await session.exec(select(User).where(User.id == user_id))
    # user = result.first()
    # if not user or user.is_deleted:
    #     raise HTTPException(status_code=401, detail="User not found or deleted")
    # 구글 토큰 체크 대신에 임시 유저 반환
    user = User(id=uuid4(), email="test@example.com", is_deleted=False)
    return user

