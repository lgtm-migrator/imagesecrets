"""Router for the user operation."""
import datetime as dt

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from image_secrets.api import dependencies, exceptions
from image_secrets.api.schemas import Token
from image_secrets.backend import users
from image_secrets.backend.constants import (
    ALGORITHM,
    SECRET_KEY,
    TOKEN_EXPIRATION_MINUTES,
)
from image_secrets.backend.database import models, schemas
from image_secrets.backend.util.main import extract_field_from_integrity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(
    tags=["users"],
    dependencies=[Depends(dependencies.get_settings)],
)


def create_access_token(data: dict, minutes: int = TOKEN_EXPIRATION_MINUTES):
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    session: AsyncSession = Depends(dependencies.get_session),
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
    user = await users.get(session, username=payload["sub"])
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    session: AsyncSession = Depends(dependencies.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    user = await users.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.post("/users/register", response_model=schemas.User)
async def register(
    user: schemas.UserCreate,
    session: AsyncSession = Depends(dependencies.get_session),
):
    try:
        db_user = await users.create(session, user)
    except IntegrityError as e:
        field = extract_field_from_integrity(e.args[0])
        raise exceptions.DetailExists(
            status_code=409,
            message="account detail already exists",
            field=field,
        )
    return db_user
