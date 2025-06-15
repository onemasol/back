from dto.chat_dto import ChatRequest
from db.entity.chat_log import ChatLog
from sqlmodel import Session
from uuid import uuid4
from datetime import datetime

def handle_chat(request: ChatRequest, db: Session) -> str:
    # (1) 사용자의 질문 저장
    user_log = ChatLog(
        chat_id=uuid4(),
        session_id=request.session_id,
        user_id=request.user_id,
        message=request.message,
        role="user",
        agent_type=None,
        step_order=0,
        is_final_response=False,
        description="User input",
        created_at=datetime.utcnow()
    )
    db.add(user_log)
    db.commit()

    # (2) 여기에서 실제 RAG / LangGraph 호출을 한다고 가정
    response_text = f"🤖 (가짜 응답) '{request.message}'에 대한 응답입니다."

    # (3) 에이전트 응답 저장
    assistant_log = ChatLog(
        chat_id=uuid4(),
        session_id=request.session_id,
        user_id=request.user_id,
        message=response_text,
        role="assistant",
        agent_type="default",
        step_order=1,
        is_final_response=True,
        description="자동 생성 응답",
        created_at=datetime.utcnow()
    )
    db.add(assistant_log)
    db.commit()

    return response_text
