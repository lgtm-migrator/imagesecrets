"""CRUD operations with user."""
from __future__ import annotations

from sqlalchemy import select, orm
from sqlalchemy.ext.asyncio import AsyncSession

from image_secrets.backend.database import models, schemas
from image_secrets.backend.util import password


async def get(session: AsyncSession, username: str) -> models.User:
    """Return a user registered in a database.

    :param session: Database session
    :param username: User's username

    """
    result = await session.execute(
        select(models.User)
        .where(models.User.username == username)
        .options(
            orm.selectinload(models.User.decoded_images),
            orm.selectinload(models.User.encoded_images),
        ),
    )
    r = result.scalars().first()
    return r


async def create(session: AsyncSession, user: schemas.UserCreate):
    """Create a new user.

    :param session: Database session
    :param user: The schema of the new user.

    """
    hashed_password = password.hash_(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password.decode(),
    )
    async with session.begin():
        session.add(db_user)
        await session.commit()
    await session.refresh(db_user)
    return db_user
