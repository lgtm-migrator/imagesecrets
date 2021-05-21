"""Router for current user.

Note: manager dependency is in every route because access to the current user information is needed.
    github issue link: https://github.com/tiangolo/fastapi/issues/424#issuecomment-584169213

"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from tortoise.exceptions import IntegrityError

from image_secrets.api import dependencies, exceptions
from image_secrets.api.routers.users.main import manager
from image_secrets.backend.database.user import crud, models, schemas
from image_secrets.backend.util.main import parse_integrity

router = APIRouter(
    prefix="/users",
    tags=["me"],
    dependencies=[Depends(dependencies.get_config), Depends(manager)],
)


@router.get("/me", response_model=schemas.User)
async def get(
    current_user: models.User = Depends(manager),
):
    return await schemas.User.from_tortoise_orm(current_user)


@router.patch("/me", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User)
async def patch(
    update_schema: schemas.UserUpdate,
    current_user: models.User = Depends(manager),
):
    try:
        user = await crud.update(
            current_user.id,
            **update_schema.dict(exclude_unset=True),
        )
    except IntegrityError as e:
        field, value = parse_integrity(error_message=e)
        raise exceptions.DetailExists(
            status_code=status.HTTP_409_CONFLICT,
            message="account detail already exists",
            field=field,
            value=value,
        ) from e
    return await schemas.User.from_tortoise_orm(user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    current_user: models.User = Depends(manager),
):
    await crud.delete(current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
