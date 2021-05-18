"""CRUD operations with user.

selectinload docs: https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#asyncio-orm-avoid-lazyloads

"""
from __future__ import annotations

from typing import Optional, Union

from sqlalchemy import delete as sql_delete
from sqlalchemy import orm, select
from sqlalchemy.ext.asyncio import AsyncSession

from image_secrets.backend.database import models, schemas, util
from image_secrets.backend.util import password


async def get(
    session: AsyncSession,
    value: Union[int, str],
    column: str = "id",
) -> Optional[models.User]:
    """Return User's model stored in a database.

    :param session: Database session
    :param value: User's value in the column
    :param column: Column of knows database value

    """
    column = getattr(models.User, column)
    result = await util.execute(
        session,
        select(models.User)
        .where(column == value)
        .options(
            orm.selectinload(models.User.decoded_images),
            orm.selectinload(models.User.encoded_images),
        ),
    )
    return result.first()


async def get_value(
    session: AsyncSession,
    value: str,
    column: str,
    result_column: str,
) -> str:
    """Return user's value stored in a database column.

    :param session: Database session
    :param value: User's known value in the column
    :param column: Column of the known database value
    :param result_column: One column value to return instead of the full user model

    """
    column = getattr(models.User, column)
    result_column = getattr(models.User, result_column)
    result = await util.execute(session, select(result_column).where(column == value))
    return result.first()


async def create(session: AsyncSession, user: schemas.UserCreate) -> models.User:
    """Create a new user.

    :param session: Database session
    :param user: The schema of the new user

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
    # need to get new user object so that selectinload gets image data
    # pydantic would not be able to parse image data when returning response
    return await get(session, user.username, "username")


async def delete(session: AsyncSession, user_id: int):
    """Delete a user.

    :param session: Database session
    :param user_id: User's database id

    """
    await util.execute(
        session,
        sql_delete(models.User).where(models.User.id == user_id),
    )
    await session.commit()


async def update(session: AsyncSession, user_id: int):
    ...
