"""Session wide fixtures."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, Generator, Optional

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from imagesecrets.schemas import UserCreate

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch
    from fastapi_mail import FastMail
    from numpy.typing import ArrayLike
    from py.path import local
    from pytest_mock import MockFixture

    from imagesecrets.config import Settings
    from imagesecrets.database.image.models import DecodedImage, EncodedImage
    from imagesecrets.database.image.services import ImageService
    from imagesecrets.database.token.services import TokenService
    from imagesecrets.database.user.models import User
    from imagesecrets.database.user.services import UserService


@pytest.fixture(autouse=True)
def api_settings(
    request,
    tmpdir: local,
    monkeypatch: MonkeyPatch,
) -> Optional[Settings]:
    """Return settings for testing environment."""
    if "disable_autouse" in set(request.keywords):
        return

    monkeypatch.setenv(
        "DATABASE_URL",
        "postgres://username:password@test_database:5432/imagesecrets",
    )
    monkeypatch.setenv("SECRET_KEY", "test_secret_key" * 10)
    monkeypatch.setenv("ICON_URL", "https://www.test_icon_url.com")
    monkeypatch.setenv("SWAGGER_URL", "https://www.test_swagger_url.com")
    monkeypatch.setenv("REDOC_URL", "https://www.test_redoc_url.com")
    monkeypatch.setenv("REPOSITORY_URL", "https://www.test_repository_url.com")

    monkeypatch.setenv("MAIL_USERNAME", "test_username")
    monkeypatch.setenv("MAIL_PASSWORD", "test_password")
    monkeypatch.setenv("MAIL_PORT", "0")
    monkeypatch.setenv("MAIL_SERVER", "test_server")

    from imagesecrets.config import settings

    return settings


@pytest.fixture(scope="session")
def app_name(api_settings) -> str:
    """Return the default app name, specified in the Settings BaseModel."""
    return api_settings.app_name


@pytest.fixture(scope="function", autouse=True)
def patch_tasks(request, monkeypatch, api_settings: Settings) -> None:
    """Patch tasks with dummy functions."""
    if "disable_autouse" in set(request.keywords):
        return

    from imagesecrets.api import tasks

    async def clear_tokens():
        """Test function to clear tokens."""

    monkeypatch.setattr(tasks, "clear_tokens", lambda: clear_tokens())


@pytest.fixture(scope="function", autouse=True)
def email_client(
    request,
    monkeypatch: MonkeyPatch,
    api_settings: Settings,
) -> FastMail | None:
    """Return test email client."""
    if "disable_autouse" in set(request.keywords):
        return

    from imagesecrets.api import dependencies

    fm = dependencies.get_mail()

    fm.config.SUPPRESS_SEND = 1
    fm.config.USE_CREDENTIALS = False

    monkeypatch.setattr(dependencies, "get_mail", lambda: fm)

    return dependencies.get_mail()


@pytest.fixture()
def api_client(api_settings: Settings) -> Generator[TestClient, None, None]:
    """Return api test client connected to fake database."""
    from imagesecrets.interface import app

    # testclient __enter__ and __exit__ deals with event loop
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="session")
def database_session(mocker: MockFixture):
    session = mocker.Mock()
    session.execute = mocker.AsyncMock()
    return session


@pytest.fixture(scope="session")
def user_service(database_session) -> UserService:
    return UserService(session=database_session)


@pytest.fixture(scope="session")
def image_service(database_session) -> ImageService:
    return ImageService(session=database_session)


@pytest.fixture(scope="session")
def token_service(database_session) -> TokenService:
    return TokenService(session=database_session)


@pytest.fixture(scope="function")
def insert_user(user_service) -> User:
    """Return user inserted into a clean database."""
    user = UserCreate(
        username="username",
        email="user@example.com",
        password="password",
    )

    user = asyncio.run(user_service.create(user=user))

    return user


@pytest.fixture(scope="function")
def auth_token(
    api_client: TestClient,
    insert_user: User,
    mocker: MockFixture,
) -> tuple[dict[str, str], User]:
    """Return authorized user and a token."""
    mocker.patch("image_secrets.backend.password.auth", return_value=True)
    response = api_client.post(
        "/users/login",
        data={
            "username": insert_user.username,
            "password": insert_user.password_hash,
        },
    ).json()

    token_header = {
        "authorization": f'{response["token_type"].capitalize()} {response["access_token"]}',
    }
    return token_header, insert_user


@pytest.fixture(scope="function")
def insert_decoded(api_client: TestClient, insert_user: User) -> DecodedImage:
    """Return decoded_image inserted into a clean database."""
    from imagesecrets.database.image.models import DecodedImage

    img = DecodedImage(
        filename="test_filename",
        image_name="test_image_name",
        message="test_message",
        delimiter="test_delimiter",
        lsb_amount=2,
        owner_id=insert_user.id,
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(img.save())

    return img


@pytest.fixture(scope="function")
def insert_encoded(api_client: TestClient, insert_user: User) -> EncodedImage:
    """Return encoded_image inserted into a clean database."""
    from imagesecrets.database.image.models import EncodedImage

    img = EncodedImage(
        filename="test_filename",
        image_name="test_image_name",
        message="test_message",
        delimiter="test_delimiter",
        lsb_amount=2,
        owner_id=insert_user.id,
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(img.save())

    return img


@pytest.fixture(scope="session")
def test_image_path() -> Path:
    """Return the path to the test.png image."""
    fp: Path = Path(__file__).parent / "test.png"
    assert fp.is_file()
    return fp


@pytest.fixture(scope="session")
def api_image_file(
    test_image_path: Path,
) -> dict[str, tuple[str, bytes, str]]:
    """Return the dict with file needed to use post requests."""
    return {
        "file": (
            test_image_path.name,
            test_image_path.open("rb").read(),
            "image/png",
        ),
    }


@pytest.fixture(scope="session")
def test_image_array(
    test_image_path: Path,
) -> ArrayLike:
    """Return numpy array of the test image."""
    with Image.open(test_image_path).convert("RGB") as img:
        array = np.array(img, dtype=np.uint8)
    return array


@pytest.fixture(scope="session")
def delimiter_array() -> ArrayLike:
    """Return a delimiter array, string form = 'dlm'."""
    return np.array(
        (
            [0],
            [1],
            [1],
            [0],
            [0],
            [1],
            [0],
            [0],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [0],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
        ),
    )
