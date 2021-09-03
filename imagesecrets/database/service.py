"""Database service."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def asyncpg_engine_url(db_url: str) -> str:
    """Return Database URL with asyncpg engine.

    :param db_url: Base database URL

    """
    split = db_url.split(":")
    split[0] = f"{split[0]}ql+asyncpg"
    return ":".join(split)


class Database:
    """Database service.

    :param db_url: Database connection url.

    """

    def __init__(self, db_url: str) -> None:
        """Construct the class."""
        db_url = asyncpg_engine_url(db_url)

        self._engine = create_async_engine(db_url, future=True, echo=True)
        self._async_session = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def get_session(self) -> AsyncSession:
        """Return database session."""
        async with self._async_session() as session:
            return session


class DatabaseService:
    def __init__(self, session: AsyncSession):
        self._session = session
