"""API dependencies."""
from __future__ import annotations

import functools as fn

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from image_secrets.api import config
from image_secrets.backend.constants import ALGORITHM, SECRET_KEY
from image_secrets.backend.database import user_crud
from image_secrets.backend.database.base import async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@fn.cache
def get_settings():
    """Return api settings."""
    return config.Settings()


async def get_session() -> AsyncSession:
    """Return an asynchronous database session."""
    async with async_session() as session:
        yield session


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    user = await user_crud.get(session, value=payload["sub"], column="username")
    return user


__all__ = [
    "get_settings",
]
