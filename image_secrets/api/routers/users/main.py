"""Router for the user operation."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from image_secrets.api import dependencies, exceptions
from image_secrets.api.routers.users import me
from image_secrets.api.schemas import Token
from image_secrets.backend.database import schemas, user_crud
from image_secrets.backend.util import login, main

router = APIRouter(
    tags=["users"],
    dependencies=[Depends(dependencies.get_settings)],
)

router.include_router(me.router)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    session: AsyncSession = Depends(dependencies.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    user = await login.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = login.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/register", response_model=schemas.User)
async def register(
    user: schemas.UserCreate,
    session: AsyncSession = Depends(dependencies.get_session),
):
    try:
        db_user = await user_crud.create(session, user)
    except IntegrityError as e:
        field = main.extract_field_from_integrity(e.args[0])
        raise exceptions.DetailExists(
            status_code=409,
            message="account detail already exists",
            field=field,
        )
    return db_user
