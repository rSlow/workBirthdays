from sqlalchemy import select, desc

from workBirthdays.core.db import dto
from workBirthdays.core.db import models as db
from workBirthdays.core.db.dao.base import BaseDao


class EventLogDao(BaseDao[db.LogEvent]):
    async def get_last_by_user(
            self, user_id: int, data: str | None, offset: bool = True
    ) -> dto.LogEvent | None:
        q = (select(self.model)
             .where(self.model.user_id == user_id)
             .order_by(desc(self.model.dt))
             .limit(1))
        if data is not None:
            q = q.where(self.model.data == data)
        if offset is True:
            q = q.offset(1)
            # logging event before selecting, need to select previous
        res = await self.session.scalars(q)
        event = res.one_or_none()
        if event:
            return event.to_dto()

    async def write_event(self, event: dto.LogEvent) -> None:
        self.session.add(
            db.LogEvent(
                event_type=event.type_,
                chat_id=event.chat_id,
                dt=event.dt,
                user_id=event.user_id,
                content_type=event.content_type,
                data=event.data
            )
        )
        await self.commit()
