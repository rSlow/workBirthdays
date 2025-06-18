from typing import Any

from sqlalchemy import select, func, delete, update

from workBirthdays.core.db import models as db, dto
from workBirthdays.core.db.dao.base import BaseDao


class SubscriptionDao(BaseDao[db.Subscription]):
    async def add(self, subscription: dto.Subscription):
        exists = await self.session.scalars(
            select(func.count(self.model.id))
            .filter(self.model.user_id == subscription.user_id)
            .filter(self.model.url == subscription.url)
        )
        if exists.one() != 0:
            raise SubAlreadyExistsError(subscription=subscription)  # TODO

        db_sub = db.Subscription(
            url=subscription.url, name=subscription.name,
            user_id=subscription.user_id, frequency=subscription.frequency,
        )
        self.session.add(db_sub)
        await self.commit()
        await self.session.refresh(db_sub)
        return db_sub.to_dto()

    async def delete(self, subscription_id: int):
        await self.session.execute(
            delete(self.model).filter(self.model.id == subscription_id)
        )
        await self.commit()

    async def get_all_user_subscriptions(self, user_id: int):
        res = await self.session.scalars(
            select(self.model).filter(self.model.user_id == user_id)
        )
        return [sub.to_dto() for sub in res.all()]

    async def get_active_user_subscriptions(self, user_id: int):
        res = await self.session.scalars(
            select(self.model)
            .filter(self.model.user_id == user_id)
            .filter_by(is_active=True)
        )
        return [sub.to_dto() for sub in res.all()]

    async def deactivate_user_subscriptions(self, user_id: int):
        await self.session.execute(
            update(self.model)
            .where(self.model.user_id == user_id)
            .values(is_active=False)
        )
        await self.commit()

    async def get(self, sub_id: int):
        return (await self._get_by_id(sub_id)).to_dto()

    async def _set_value(self, id_: int, attr: str, value: Any) -> dto.Subscription:
        kwargs = {attr: value}
        res = await self.session.execute(
            update(self.model)
            .where(self.model.id == id_)
            .values(**kwargs)
            .returning(self.model)
        )
        await self.commit()
        await self.session.flush()
        return res.scalar().to_dto()

    async def set_is_active(self, subscription_id: int, is_active: bool):
        return await self._set_value(subscription_id, "is_active", is_active)

    async def set_name(self, subscription_id: int, name: str):
        return await self._set_value(subscription_id, "name", name)

    async def set_frequency(self, subscription_id: int, frequency: int):
        return await self._set_value(subscription_id, "frequency", frequency)
