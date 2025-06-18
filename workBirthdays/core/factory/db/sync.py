import logging

from sqlalchemy import Engine as SyncEngine, create_engine as create_sync_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker as sync_sessionmaker, Session as SyncSession

from workBirthdays.core.config.models.db import DBConfig

logger = logging.getLogger(__name__)


def create_pool(db_config: DBConfig) -> sync_sessionmaker[SyncSession]:
    engine = create_engine(db_config)
    return create_session_maker(engine)


def create_engine(db_config: DBConfig) -> SyncEngine:
    logger.info("created sync db engine for %s", db_config)
    return create_sync_engine(
        url=make_url(db_config.sync_uri),
        echo=db_config.echo
    )


def create_session_maker(
        engine: SyncEngine
) -> sync_sessionmaker[SyncSession]:
    pool: sync_sessionmaker[SyncSession] = sync_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )
    return pool
