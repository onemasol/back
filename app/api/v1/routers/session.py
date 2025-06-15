from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession
from db.session import get_db
from dto.session_dto import CreateSessionRequest, SessionResponse
from services import session_service

router = APIRouter()

@router.post("/session", response_model=SessionResponse)
def create(data: CreateSessionRequest, db: DBSession = Depends(get_db)):
    return session_service.create_session(db, data)

@router.get("/session", response_model=list[SessionResponse])
def list_sessions(user_id: str, db: DBSession = Depends(get_db)):
    return session_service.get_user_sessions(db, user_id)

@router.delete("/session/{session_id}")
def delete(session_id: str, db: DBSession = Depends(get_db)):
    if not session_service.delete_session(db, session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}
