"""Base database module."""
from __future__ import annotations

from typing import TYPE_CHECKING

from imagesecrets.config import settings
from imagesecrets.database.service import Database
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base, declared_attr

if TYPE_CHECKING:
    from fastapi import FastAPI


class Base:
    """SQLAlchemy base class."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Return database table name."""
        return cls.__name__.lower()

    @declared_attr
    def __mapper_args__(cls) -> dict[str, bool]:
        """Return mapper args dictionary."""
        return {"eager_defaults": True}

    id = Column(Integer, primary_key=True)

    created = Column(DateTime, server_default=func.now())
    updated = Column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


Base = declarative_base(cls=Base)
database = Database(db_url=settings.pg_dsn)


def init(app: FastAPI) -> None:
    """Initialize SQLAlchemy on startup."""

    @app.on_event("startup")
    async def startup():
        async with database._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
