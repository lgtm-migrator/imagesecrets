"""CRUD operations with a Token."""
from __future__ import annotations

from tortoise.exceptions import DoesNotExist, IntegrityError

from image_secrets.backend import password
from image_secrets.backend.database.token.models import Token
from image_secrets.backend.util.main import token_url


async def create(token_hash: str, owner_id: int) -> Token:
    """Create a new token and insert it's hash into database.

    :param token_hash: Hash of the token to insert
    :param owner_id: User foreign key

    """
    token = await Token.create(token_hash=token_hash, owner_id=owner_id)
    return token


async def create_new(owner_id: int) -> str:
    """Ensure that a new token is created.

    If a token already exists, delete it and create a new one

    :param owner_id: User foreign key

    """
    token = token_url()
    token_hash = password.hash_(token)
    try:
        await create(token_hash=token_hash, owner_id=owner_id)
    except IntegrityError:
        await delete(owner_id=owner_id)
        await create(token_hash=token_hash, owner_id=owner_id)
    return token


async def delete(owner_id: int) -> None:
    """Delete a token from database.

    :param owner_id: User foreign key tied to the token

    """
    await Token.filter(owner_id=owner_id).delete()


async def get_owner_id(token: str) -> int:
    """Return owner_id of a token.

    :param token: The token to check

    :raises DoesNotExist: if no token_hash matches the provided token

    """
    tokens = await Token.all().only("token_hash", "owner_id")
    gen = (t.owner_id for t in tokens if password.auth(token, t.token_hash))  # type: ignore
    try:
        user_id = next(gen)
    except StopIteration as e:
        raise DoesNotExist(
            f"the token {token!r} does not match any token in database",
        ) from e
    assert isinstance(user_id, int)
    return user_id
