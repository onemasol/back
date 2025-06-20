from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings


# ✅ asyncpg 기반 비동기 엔진 생성
print("🔍 실제 연결되는 DB:", settings.DB_URL)
engine = create_async_engine(settings.DB_URL, echo=True, future=True)

# ✅ 세션 메이커 정의
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ✅ 초기화 함수 (비동기 버전)
async def init_db():
    """
    Initialize the database (create tables).
    """
    #import app.db.entity.user
    #import app.db.entity.event
    #import app.db.entity.task
    #from app.db.entity.document import Document
    print("🔄 Initializing database...")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Database initialized successfully.")
