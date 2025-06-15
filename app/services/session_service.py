from sqlmodel import Session as DBSession, select
from db.entity.chat_session import Session
from db.entity.chat_log import ChatLog
from dto.session_dto import CreateSessionRequest
from datetime import datetime

def create_session(db: DBSession, data: CreateSessionRequest):
    new_session = Session(user_id=data.user_id, title=data.title)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def get_user_sessions(db: DBSession, user_id: str):
    return db.exec(select(Session).where(Session.user_id == user_id)).all()

def delete_session(db: DBSession, session_id: str):
    session = db.get(Session, session_id)
    if session:
        db.delete(session)
        db.commit()
        return True
    return False
