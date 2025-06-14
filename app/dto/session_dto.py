from pydantic import BaseModel
from typing import Optional

class CreateSessionRequest(BaseModel):
    user_id: str
    title: Optional[str] = "New Chat"

class SessionResponse(BaseModel):
    session_id: str
    title: str
    created_at: str
    last_updated: str
