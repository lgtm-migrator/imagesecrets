"""Utlity functions connected to users."""
from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from jose import jwt

from image_secrets.backend.constants import (
    SECRET_KEY,
    ALGORITHM,
    TOKEN_EXPIRATION_MINUTES,
)
from image_secrets.backend.database import models, user_crud
from image_secrets.backend.util import password

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def create_access_token(data: dict, minutes: int = TOKEN_EXPIRATION_MINUTES):
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=minutes)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate(
    session: AsyncSession,
    username: str,
    plain_password: str,
) -> models.User:
    user_model = await user_crud.get(session, username)
    if password.auth(plain_password, user_model.password):
        return user_model
