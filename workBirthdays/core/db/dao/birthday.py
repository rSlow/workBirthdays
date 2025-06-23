from datetime import date
from uuid import UUID

from sqlalchemy import delete, select, and_, extract, func

from workBirthdays.core.db import dto
from workBirthdays.core.db import models as db
from workBirthdays.core.db.dao.base import BaseDao


class BirthdayDao(BaseDao[db.Birthday]):
    async def update(self, birthdays: list[dto.Birthday], user_id: int):
        await self.session.execute(
            delete(self.model)
            .filter(self.model.uuid.in_([birthday.uuid for birthday in birthdays]))
            .filter(self.model.user_id == user_id)
        )
        models = [
            self.model(
                fio=birthday.fio, date=birthday.date, uuid=birthday.uuid,
                post=birthday.post, rank=birthday.rank, user_id=user_id
            )
            for birthday in birthdays
        ]
        self.session.add_all(models)
        await self.commit()

    async def delete_all_from_user(self, user_id: int):
        await self.session.execute(
            delete(self.model)
            .filter(self.model.user_id == user_id)
        )
        await self.commit()

    async def delete(self, birthday_uuid: UUID):
        res = await self.session.execute(
            select(func.count(self.model.uuid))
            .filter(self.model.uuid == birthday_uuid)
        )
        birthday_rows_count = res.scalar_one()

        if birthday_rows_count == 0:
            return False

        await self.session.execute(
            delete(self.model)
            .filter(self.model.uuid == birthday_uuid)
        )
        await self.commit()
        return True

    async def get_by_date(self, d: date, user_id: int):
        res = await self.session.scalars(
            select(self.model)
            .where(
                and_(
                    extract('month', self.model.date) == d.month,
                    extract('day', self.model.date) == d.day,
                    self.model.user_id == user_id
                ),
            )
        )
        return [birthday.to_dto() for birthday in res.all()]
