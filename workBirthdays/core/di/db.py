from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from workBirthdays.core.config.models import BaseConfig
from workBirthdays.core.config.models.db import DBConfig
from workBirthdays.core.factory.db.a_sync import create_engine, create_session_maker


class DbProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_config(self, base_config: BaseConfig) -> DBConfig:
        return base_config.db

    @provide
    async def get_engine(self, db_config: DBConfig) -> AsyncIterable[AsyncEngine]:
        engine = create_engine(db_config)
        yield engine
        await engine.dispose(True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session
