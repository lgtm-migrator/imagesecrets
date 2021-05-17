"""Router for current user.

Note: get_current_user dependency is in every function because access to the current user is needed.
    github issue link: https://github.com/tiangolo/fastapi/issues/424#issuecomment-584169213

"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from image_secrets.api.dependencies import get_settings, get_current_user, get_session
from image_secrets.backend.database import schemas, models, user_crud

router = APIRouter(
    prefix="/users",
    tags=["me"],
    dependencies=[Depends(get_settings), Depends(get_current_user)],
)


@router.get("/me", response_model=schemas.User)
async def get(
    current_user: models.User = Depends(get_current_user),
):
    return current_user


@router.patch("/me", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User)
async def patch(
    attr: str = Query(
        ...,
        alias="attribute",
        description="Account detail to edit",
    ),
    new_value: str = Query(
        ...,
        alias="new-value",
        description="New value of specified attribute",
    ),
    current_user: models.User = Depends(get_current_user),
):
    print(attr, new_value)
    return current_user


@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete(
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    await user_crud.delete(session, current_user.username)
