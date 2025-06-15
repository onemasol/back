from app.db.entity.chat_log import ChatLog
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import uuid4
from uuid import UUID
from datetime import datetime
from sqlmodel import select
from app.dto.agent_log_dto import ChatTransactionLog


async def save_transaction_log(data: ChatTransactionLog, db: AsyncSession):
    log = ChatLog(
        chat_id=uuid4(),
        session_id=data.session_id,
        user_id=data.user_id,
        task_id=data.task_id,
        message=data.user_message,
        role="user",
        agent_type=data.agent_type,
        step_order=0,
        is_final_response=True,
        embedding_id=data.embedding_id,
        description=data.agent_response,
        created_at=datetime.utcnow()
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

async def get_transaction_logs_by_session(session_id: UUID, db: AsyncSession):
    statement = (
        select(ChatLog)
        .where(ChatLog.session_id == session_id)
        .where(ChatLog.is_final_response == True)
        .order_by(ChatLog.created_at)
    )
    results = await db.exec(statement)
    return results.all()