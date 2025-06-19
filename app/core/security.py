from fastapi import Header, HTTPException
from datetime import datetime, timedelta, timezone
from typing import Union, Any
from jose import jwt, JWTError
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer



def get_token_from_header(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    return authorization[len("Bearer "):]


def _create_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
    """
    주어진 만료 시간을 바탕으로 JWT를 생성하는 내부 헬퍼 함수
    """
    # UTC 시간대를 명시적으로 사용하여 예상치 못한 시간대 오류를 방지 (utcnow()보다 권장)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_access_token(subject: Union[str, Any]) -> str:
    """
    Access Token 생성 (config.py에 설정된 ACCESS_TOKEN_EXPIRE_MINUTES 사용)
    """
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(subject, expires_delta)


def create_refresh_token(subject: Union[str, Any]) -> str:
    """
    Refresh Token 생성 (config.py에 설정된 REFRESH_TOKEN_EXPIRE_MINUTES 사용)
    """
    expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return _create_token(subject, expires_delta)

def decode_access_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])