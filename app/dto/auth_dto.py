"""
OAuth & JWT 관련 DTO 정의
------------------------
• 클라이언트 → 서버 : Google ID 토큰을 보낼 때 OAuthLoginDTO
• 서버 → 클라이언트 : JWT를 담은 TokenDTO
"""

from pydantic import BaseModel
from typing import Literal
from typing import Optional  # Optional을 임포트합니다.

class GoogleToken(BaseModel):
    """구글 id_token을 받기 위한 DTO"""
    id_token: str

class LoginResponse(BaseModel):
    """로그인 성공 시 반환할 access_token DTO"""
    access_token: str
    token_type: str = "bearer"
    

class GoogleTokenInfo(BaseModel):
    """Google id_token 검증 후 얻게 되는 사용자 정보 DTO"""
    # --- 필수 인증 정보 ---
    iss: str
    sub: str
    azp: str
    aud: str
    iat: int
    exp: int
    email: str
    email_verified: bool
    # --- 선택적 프로필 정보 ---
    name: Optional[str] = None
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = None