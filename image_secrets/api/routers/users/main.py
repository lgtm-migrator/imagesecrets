"""Router for the user operation."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from tortoise.exceptions import DoesNotExist, IntegrityError

from image_secrets.api import dependencies
from image_secrets.api.exceptions import DetailExists, NotAuthenticated
from image_secrets.api.schemas import Token
from image_secrets.backend.database.user import crud, schemas
from image_secrets.backend.util.main import parse_integrity

config = dependencies.get_config()
router = APIRouter(
    tags=["users"],
    dependencies=[Depends(dependencies.get_config)],
)
manager = LoginManager(config.secret_key, "/login")
manager.not_authenticated_exception = NotAuthenticated


@manager.user_loader
async def user_loader(username: str):
    try:
        return await crud.get(crud.DBIdentifier(column="username", value=username))
    except DoesNotExist as e:
        raise NotAuthenticated(status_code=status.HTTP_404_NOT_FOUND) from e


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    auth = await crud.authenticate(form_data.username, form_data.password)
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
        )

    access_token = manager.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/users/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
async def register(user: schemas.UserCreate):
    try:
        db_user = await crud.create(user)
    except IntegrityError as e:
        field, value = parse_integrity(error_message=e)
        raise DetailExists(
            status_code=status.HTTP_409_CONFLICT,
            message="account detail already exists",
            field=field,
            value=value,
        ) from e
    return await schemas.User.from_tortoise_orm(db_user)
