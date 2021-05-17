"""Router for current user."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from image_secrets.api.dependencies import get_settings, get_current_user
from image_secrets.backend.database import schemas, models

router = APIRouter(
    tags=["me"],
    dependencies=[Depends(get_settings)],
)


@router.get("/users/me", response_model=schemas.User)
async def get(
    current_user: models.User = Depends(get_current_user),
):
    return current_user
