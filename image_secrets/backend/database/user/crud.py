"""CRUD operations with a user in database."""
from __future__ import annotations

from typing import Any, NamedTuple, Optional, Union

from image_secrets.backend.database.user import models, schemas
from image_secrets.backend.util import password


class DBIdentifier(NamedTuple):
    """Identifier namedtuple for User in a database.

    :param column: Column of a known user value
    :param value: Value of the column

    """

    column: str
    value: Union[int, str]


async def get(identifier: DBIdentifier) -> Optional[models.User]:
    """Return User's model stored in a database.

    :param identifier: DBIdentifier to identify which user to return

    """
    identifier_dict = {identifier.column: identifier.value}
    return await models.User.get(**identifier_dict)


async def create(user: schemas.UserCreate) -> models.User:
    """Insert a new user.

    :param user: The schema of the new user

    """
    hashed = password.hash_(user.password.get_secret_value())
    db_user = await models.User.create(
        **user.dict(exclude_unset=True),
        password_hash=hashed,
    )
    return db_user


async def delete(user_id: int) -> None:
    """Delete a user from database.

    :param user_id: User's database id

    """
    await models.User.filter(id=user_id).delete()


async def update(user_id: int, **attributes: Any) -> models.User:
    """Update user's credentials in the database.

    :param user_id: User's database id
    :param attributes: Keyword arguments with attributes to update

    """
    await models.User.filter(id=user_id).update(**attributes)
    return await get(DBIdentifier(column="id", value=user_id))


async def authenticate(username: str, password_: str) -> bool:
    """Authenticate a user login.

    :param username: User's username
    :param password_: User's password

    """
    hashed = await models.User.filter(username=username).values_list(
        "password_hash",
        flat=True,
    )
    try:
        return password.auth(password_, hashed[0])
    except IndexError:
        return False
