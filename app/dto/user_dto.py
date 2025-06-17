from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import datetime as dt
from uuid import UUID # UUID 임포트
class UserSignupDTO(BaseModel):
    access_token: str  # from Google OAuth

class UserCreateDTO(BaseModel):
    email:    str    = Field(..., description="이메일")
    name:   str    = Field(..., description="닉네임")

class UserLoginDTO(BaseModel):
    access_token: str

class UserMeUpdateDTO(BaseModel):
    email: str
    name: Optional[str] = Field(None, max_length=30)

class UserPublicDTO(BaseModel):
    id: UUID
    email: str
    name: Optional[str]
    is_deleted: bool
    #created_at: dt.datetime
    #updated_at: dt.datetime
