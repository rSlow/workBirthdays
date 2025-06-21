from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from workBirthdays.core.db import models as db, dto
from workBirthdays.core.db.dao.base import BaseDao
from workBirthdays.core.db.models.user import UsersRoles


class RoleDao(BaseDao[db.Role]):
    async def get_all(self):
        res = await self.session.scalars(select(self.model))
        return [role.to_dto() for role in res.all()]

    async def get(self, role_id: int):
        db_role = await self._get_by_id(role_id)
        return db_role.to_dto()

    async def get_by_name(self, role_name: str):
        db_role = await self.session.scalars(
            select(self.model)
            .where(self.model.name == role_name)
        )
        return db_role.one().to_dto()

    async def delete(self, role_id: int):
        await self.session.execute(
            delete(self.model)
            .where(self.model.id == role_id)
        )
        await self.commit()

    async def add(self, role: dto.UserRole):
        kwargs = {
            "name": role.name,
            "alias": role.alias,
        }
        res = await self.session.execute(
            insert(self.model)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(self.model.name,),
                set_=kwargs,
                where=self.model.name == role.name
            )
            .returning(self.model)
        )
        await self.commit()
        await self.session.flush()
        return res.scalar_one().to_dto()

    async def add_user(self, role_id: int, user_id: int):
        await self.session.execute(
            insert(UsersRoles)
            .values(
                role_id=role_id,
                user_id=user_id,
            )
        )
        await self.commit()

    async def remove_user(self, role_id: int, user_id: int):
        await self.session.execute(
            delete(UsersRoles)
            .filter_by(role_id=role_id, user_id=user_id)
        )
        await self.commit()
