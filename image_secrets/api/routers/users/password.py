"""User password API endpoint."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Response, status
from tortoise.exceptions import IntegrityError

from image_secrets.api import dependencies, exceptions, responses
from image_secrets.api.routers.users.main import manager
from image_secrets.backend.database.user import crud, models, schemas
from image_secrets.backend.util.main import parse_unique_integrity

router = APIRouter(
    prefix="/users/me",
    tags=["password"],
    dependencies=[Depends(dependencies.get_config), Depends(manager)],
    responses=...,
)


router
