from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.v1.deps import get_session
from app.services.chat_log_service import get_transaction_logs_by_session
from uuid import UUID

router = APIRouter(prefix="/agent/chat", tags=["Agent Chat"])


@router.get("/sessions/{session_id}")
async def get_session_logs(session_id: UUID, db: AsyncSession = Depends(get_session)):
    logs = await get_transaction_logs_by_session(session_id, db)
    return logs
