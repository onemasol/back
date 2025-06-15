from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.v1.deps import get_session
from app.dto.agent_log_dto import ChatTransactionLog
from app.services.chat_log_service import save_transaction_log

router = APIRouter(prefix="/agent/logs", tags=["Agent Logs"])


@router.post("")
async def log_transaction(data: ChatTransactionLog, db: AsyncSession = Depends(get_session)):
    result = await save_transaction_log(data, db)
    return result
