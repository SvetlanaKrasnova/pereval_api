from typing import Callable, Union

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from src.core.config import app_settings


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()


def create_sessionmaker(bind_engine: Union[AsyncEngine, AsyncConnection]) -> Callable[..., async_sessionmaker]:
    return async_sessionmaker(
        bind=bind_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


engine = create_async_engine(app_settings.postgres_dsn.unicode_string())

async_session = create_sessionmaker(engine)
