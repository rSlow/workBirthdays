from datetime import time

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from workBirthdays.core.db import models as db
from workBirthdays.core.db.dao.base import BaseDao


class UserNotificationDao(BaseDao[db.NotificationState]):
    async def get_user_state(self, user_id: int):
        res = await self.session.scalars(
            select(self.model)
            .where(self.model.user_id == user_id)
        )
        user = res.one_or_none()
        if user is not None:
            return user.to_dto()

    async def add_or_update_user_state(self, user_id: int, timeshift: time | None = None):
        kwargs = {
            "user_id": user_id,
            "timeshift": timeshift or time(hour=0, minute=0),
        }
        await self.session.execute(
            insert(self.model)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(self.model.user_id,),
                set_=kwargs,
                where=self.model.user_id == user_id
            )
        )
        await self.commit()
        saved_user = await self.get_user_state(user_id)
        return saved_user

    async def get_user_notifications(self, user_id: int):
        res = await self.session.scalars(
            select(db.NotificationTime)
            .join(self.model)
            .where(self.model.user_id == user_id)
        )
        return [note.to_dto() for note in res.all()]

    async def get_notification(self, notification_id: int):
        res = await self.session.scalars(
            select(db.NotificationTime)
            .where(db.NotificationTime.id == notification_id)
        )
        return res.one().to_dto()

    async def delete_notification(self, notification_id: int):
        await self.session.execute(
            delete(db.NotificationTime)
            .where(db.NotificationTime.id == notification_id)
        )
        await self.commit()

    async def add_notification(self, user_id: int, notification_time: time):
        user_state = await self.add_or_update_user_state(user_id)
        notification = db.NotificationTime(time=notification_time, user_state_id=user_state.id_)
        self.session.add(notification)
        await self.commit()
        await self.session.refresh(notification)
        return notification.to_dto()

    async def clear_notifications(self, user_id: int):
        await self.session.execute(
            delete(db.NotificationTime)
            .where(db.NotificationState.user_id == user_id)
        )
        await self.commit()
