from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class ChatSessionCreate(BaseModel):
    user_id: UUID
    session_title: Optional[str]
    current_task: Optional[str]
    current_node: Optional[str]
    metadata: Optional[dict]


class ChatLogCreate(BaseModel):
    session_id: UUID
    user_id: UUID
    task_id: Optional[UUID]
    message: str
    role: Optional[str]
    agent_type: Optional[str]
    step_order: Optional[int]
    is_final_response: Optional[bool]
    embedding_id: Optional[UUID]
    description: Optional[str]
    
class ChatRequest(BaseModel):
    session_id: UUID
    user_id: UUID
    message: str
