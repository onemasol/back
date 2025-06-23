# app/services/calendar_service.py
from fastapi import HTTPException,Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse
from sqlmodel import select
from app.db.entity.event import Event
from app.dto.event_dto import EventCreateDTO, EventRead, EventUpdateDTO
from app.api.v1.deps import get_session
from app.utils.dto_utils import dump_with_formatted_datetime
from uuid import UUID
from datetime import datetime, timezone

class CalendarService:
    """
    캘린더 CRUD 전담
    """
    async def read_events(self, session: AsyncSession, user_id: UUID):
        result = await session.execute(
            select(Event).where(Event.user_id == str(user_id)) 
        )
        events = result.scalars().all()
        return [dump_with_formatted_datetime(EventRead.from_orm(e)) for e in events]
    
    async def create_event(self, event: EventCreateDTO, user_id: UUID, session: AsyncSession = Depends(get_session)):
        event_data = event.model_dump()
        used_agents_data = event_data.pop("used_agents", None)
        # DB 모델 생성
        new_event = Event(
            **event_data,
            user_id=str(user_id),
            used_agents=used_agents_data
        )
        
        session.add(new_event)
        await session.commit()
        await session.refresh(new_event)
        
        return dump_with_formatted_datetime(EventRead.from_orm(new_event))
    
    async def read_event(self, event_id: UUID, user_id: UUID, session: AsyncSession):
        stmt = select(Event).where(Event.id == event_id, Event.user_id == str(user_id))
        result = await session.exec(stmt)
        ev = result.first()
        if not ev:
            raise HTTPException(status_code=404, detail="Event not found")
        return dump_with_formatted_datetime(EventRead.from_orm(ev))

    async def update_event(self, event_id: UUID, dto: EventUpdateDTO, user_id: UUID, session: AsyncSession):
        stmt = select(Event).where(Event.id == event_id, Event.user_id == str(user_id))
        ev = (await session.exec(stmt)).first()
        if not ev:
            raise HTTPException(status_code=404, detail="Event not found")
        for k, v in dto.dict(exclude_unset=True).items():
            setattr(ev, k, v)
        ev.updated_at = datetime.now(timezone.utc)
        session.add(ev)
        await session.commit()
        await session.refresh(ev)
        return dump_with_formatted_datetime(EventRead.from_orm(ev))

    async def delete_event(self, event_id: UUID, user_id: UUID, session: AsyncSession):
        stmt = select(Event).where(Event.id == event_id, Event.user_id == str(user_id))
        ev = (await session.exec(stmt)).first()
        if not ev:
            raise HTTPException(status_code=404, detail="Event not found")
        await session.delete(ev)
        await session.commit()
        return {"ok": True, "message": "Event deleted"}
