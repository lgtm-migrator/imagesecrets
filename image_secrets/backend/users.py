"""Module with CRUD operations connected to users."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import orm, select

from image_secrets.backend.database import models, schemas
from image_secrets.backend.util import password

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


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


async def authenticate(
    session: AsyncSession,
    username: str,
    plain_password: str,
) -> models.User:
    user = await get(session, username)
    if password.auth(plain_password, user.password):
        return user
