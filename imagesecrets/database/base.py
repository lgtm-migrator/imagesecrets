"""Base database module."""
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

engine = create_async_engine("DATABASE_URL", future=True, echo=True)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


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
