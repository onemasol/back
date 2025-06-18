from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4 # uuid 임포트
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # PG_UUID 임포트
from sqlalchemy import Column

class User(SQLModel, table=True):
    __tablename__ = "users"

    # id 타입을 UUID로 변경
    id: UUID = Field( default_factory=uuid4,
                     sa_column=Column(PG_UUID, primary_key=True, nullable=False, unique=True))
    google_user_id: Optional[str] = Field(index=True, unique=True, nullable=True, default=None)
    email: str = Field(index=True, unique=True, nullable=False)
    name: Optional[str] = Field(default=None)
    provider: str = Field(default="google", description="사용자 인증 제공자")
    is_deleted: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    region: str= Field(default="Asia/Seoul", description="사용자 지역 정보")
    is_using: bool = Field(default=True)    
    status: str = Field(default="active", description="사용자 상태")
    calendar_id: Optional[int] = Field(default=None)
    last_login_at: Optional[datetime] = Field(default_factory=datetime.utcnow)