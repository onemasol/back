from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.v1.deps import get_session, get_current_user
from app.dto.agent_log_dto import ChatTransactionLog
from app.db.entity.user import User
from app.services.chat_log_service import save_transaction_log

router = APIRouter(prefix="/agent/logs", tags=["Agent Logs"])


@router.post("")
async def log_transaction(data: ChatTransactionLog, db: AsyncSession = Depends(get_session), user: User=Depends(get_current_user)):
    result = await save_transaction_log(data, db, user.id)
    return result
