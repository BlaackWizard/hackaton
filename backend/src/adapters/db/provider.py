from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from backend.src.adapters.config_loader import DBConfig


async def get_engine(config: DBConfig) -> AsyncIterator[AsyncEngine]:
    connection_url = config.postgres_conn_url

    engine = create_async_engine(
        connection_url,
        future=True,
    )
    yield engine
    await engine.dispose()


async def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    return session_factory


async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
