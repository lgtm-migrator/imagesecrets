"""Utlity functions connected to users."""
from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from jose import jwt

from image_secrets.backend.constants import (
    ALGORITHM,
    SECRET_KEY,
    TOKEN_EXPIRATION_MINUTES,
)
from image_secrets.backend.database import user_crud
from image_secrets.backend.util import password

if TYPE_CHECKING:
    from datetime import timedelta

    from sqlalchemy.ext.asyncio import AsyncSession


def create_access_token(
    data: dict,
    minutes: timedelta = TOKEN_EXPIRATION_MINUTES,
) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + minutes
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate(
    session: AsyncSession,
    username: str,
    plain_password: str,
) -> bool:
    user_password = await user_crud.get_value(
        session,
        value=username,
        column="username",
        result_column="password",
    )
    return password.auth(plain_password, user_password)
