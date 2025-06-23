from fastapi import APIRouter
from .routers import auth, users, health, calendar, agent_log, agent_chat,agent_task,documents, tasks, agent_event

router = APIRouter()
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(calendar.router)
router.include_router(agent_log.router)
router.include_router(agent_chat.router)
router.include_router(agent_task.router)  
router.include_router(documents.router)
router.include_router(tasks.router)  # 기존의 태스크 라우터
router.include_router(agent_event.router) 
#router.include_router(agent.router)

router.include_router(health.router)      # ← 테스트용 라우터


