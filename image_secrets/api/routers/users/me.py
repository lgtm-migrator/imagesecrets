"""Router for current user.

Note: manager dependency is in every route because access to the current user information is needed.
    relevant github discussion: https://github.com/tiangolo/fastapi/issues/424#issuecomment-584169213

"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from tortoise.exceptions import IntegrityError

from image_secrets.api import dependencies, exceptions, responses
from image_secrets.api import schemas as api_schemas
from image_secrets.api.routers.users.main import manager
from image_secrets.backend import password
from image_secrets.backend.database.user import crud, models, schemas
from image_secrets.backend.util.main import parse_unique_integrity

router = APIRouter(
    prefix="/users",
    tags=["me"],
    dependencies=[Depends(dependencies.get_config), Depends(manager)],
    responses=responses.AUTHORIZATION | responses.FORBIDDEN,
)


@router.get(
    "/me",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    summary="Account information",
)
async def get(
    current_user: models.User = Depends(manager),
) -> Optional[schemas.User]:
    """Show all information connected to a User.

    \f
    :param current_user: Current user dependency

    """
    return await schemas.User.from_tortoise_orm(current_user)


@router.patch(
    "/me",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    summary="Update user credentials",
    responses=responses.CONFLICT,
)
async def patch(
    update_schema: schemas.UserUpdate,
    current_user: models.User = Depends(manager),
) -> Optional[schemas.User]:
    """Update account details

    - **username**: New account username
    - **email**: New account email

    \f
    :param update_schema: Schema with necessary information to update the user details
    :param current_user: Current user dependency

    :raises DetailExists: if either of the new values are already claimed in the database

    """
    try:
        user = await crud.update(
            current_user.id,
            **update_schema.dict(exclude_unset=True),
        )
    except IntegrityError as e:
        field, value = parse_unique_integrity(error=e)
        raise exceptions.DetailExists(
            status_code=status.HTTP_409_CONFLICT,
            message="account detail already exists",
            field=field,
            value=value,
        ) from e
    return await schemas.User.from_tortoise_orm(user)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an Account",
)
async def delete(
    current_user: models.User = Depends(manager),
) -> Optional[Response]:
    """Delete a user and all extra information connected to it.

    \f
    :param current_user: Current user dependency

    """
    await crud.delete(current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Change user password",
)
async def password(
    data: api_schemas.ChangePassword,
    current_user: models.User = Depends(manager),
) -> Optional[Response]:
    """Change account password.

    \f
    :param data: Password data
    :param current_user: Current user dependency

    """
    auth = await crud.authenticate(username=current_user.username, password_=data.old)
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect password",
        )
    hashed = password.hash_(data.new)
    await crud.update(current_user.id, password_hash=hashed)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
