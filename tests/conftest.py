"""Session wide fixtures."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO, Generator

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from tortoise.contrib.test import finalizer, initializer

from image_secrets.api import config as config_
from image_secrets.backend.database import image_models, user_models
from image_secrets.backend.util import main

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


@pytest.fixture(scope="function", autouse=True)
def api_settings(tmpdir) -> config_.Settings:
    """Return settings for the testing environment."""
    db_url = "sqlite://:memory:"
    test_settings = config_.Settings.construct(
        image_folder=str(Path(tmpdir.mkdir("images/")).absolute()),
        pg_dsn=db_url,
    )
    config_.settings = test_settings

    return config_.settings


def sqlite_parsing(error: str) -> list[str]:
    """Return parsed sqlite error message."""
    return str(error).split(":")


@pytest.fixture(scope="function")
def api_client(request, api_settings) -> Generator[TestClient, None, None]:
    """Return api test client connected to fake database."""
    main.parse_unique_integrity = sqlite_parsing

    # settings already patched by fixture
    from image_secrets.api.interface import app

    initializer(
        [user_models, image_models],
        db_url=api_settings.pg_dsn,
        app_label="models",
    )

    # testclient __enter__ and __exit__ deals with event loop
    with TestClient(app=app) as client:
        yield client

    request.addfinalizer(finalizer)


@pytest.fixture(scope="session")
def app_name() -> str:
    """Return the default app name, specified in the Settings BaseModel."""
    return config_.Settings.__dict__["__fields__"]["app_name"].default


@pytest.fixture(scope="session")
def test_image_path() -> Path:
    """Return the path to the test.png image."""
    return Path(__file__).parent / "test.png"


@pytest.fixture(scope="session")
def api_image_file(test_image_path) -> dict[str, tuple[str, BinaryIO, str]]:
    """Return the dict with file needed to use post requests."""
    return {"file": (test_image_path.name, test_image_path.open("rb"), "image/png")}


@pytest.fixture(scope="session")
def test_image_array(test_image_path: Path) -> Generator[ArrayLike, None, None]:
    """Return numpy array of the test image."""
    with Image.open(test_image_path).convert("RGB") as img:
        yield np.asarray(img, dtype=np.uint8)


@pytest.fixture(scope="session")
def random_image_arr() -> ArrayLike:
    """Return array containing data about a random image."""
    return np.random.randint(0, 255, size=(8, 8, 3), dtype=np.uint8)


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
