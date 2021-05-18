"""Router for the user operation."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from image_secrets.api import dependencies, exceptions
from image_secrets.api.schemas import Token
from image_secrets.backend.database import schemas, user_crud
from image_secrets.backend.util import login, main

router = APIRouter(
    tags=["users"],
    dependencies=[Depends(dependencies.get_settings)],
)


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(
    session: AsyncSession = Depends(dependencies.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    auth = await login.authenticate(session, form_data.username, form_data.password)
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = login.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/users/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
async def register(
    user: schemas.UserCreate,
    session: AsyncSession = Depends(dependencies.get_session),
):
    try:
        db_user = await user_crud.create(session, user)
    except IntegrityError as e:
        field, value = main.parse_integrity(error_message=e.args[0])
        raise exceptions.DetailExists(
            status_code=status.HTTP_409_CONFLICT,
            message="account detail already exists",
            field=field,
            value=value,
        )
    return db_user
