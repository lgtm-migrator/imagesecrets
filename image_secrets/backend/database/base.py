"""Main database module."""
from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise.contrib.fastapi import register_tortoise

from image_secrets.backend.database.image import models as image_models
from image_secrets.backend.database.user import models as user_models

if TYPE_CHECKING:
    from fastapi import FastAPI


def init(app: FastAPI, db_url: str) -> None:
    """Initialize database connection.

    :param app: FastAPI instance
    :param db_url: Url to database

    """
    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": [user_models, image_models]},
        generate_schemas=True,
    )
