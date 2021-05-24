"""Session wide fixtures."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from tortoise.contrib.test import finalizer, initializer

from image_secrets.api.config import Settings
from image_secrets.api.interface import app
from image_secrets.backend.database import image_models, user_models

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


@pytest.fixture(scope="session", autouse=True)
def api_client(request):
    """Return api test client with fake database."""
    db_url = "sqlite://:memory:"
    initializer([user_models, image_models], db_url=db_url, app_label="models")
    with TestClient(app) as client:
        yield client
    request.addfinalizer(finalizer)


@pytest.fixture()
def app_name() -> str:
    """Return the default app name, specified in the Settings BaseModel."""
    return Settings.__dict__["__fields__"]["app_name"].default


@pytest.fixture()
def test_image_path() -> Path:
    """Return the path to the test.png image."""
    return Path(__file__).parent / "test.png"


@pytest.fixture()
def api_image_file(test_image_path) -> dict[str, tuple[str, BinaryIO, str]]:
    """Return the dict with file needed to use post requests."""
    return {"file": (test_image_path.name, test_image_path.open("rb"), "image/png")}


@pytest.fixture()
def test_image_array(test_image_path: Path) -> ArrayLike:
    """Return numpy array of the test image."""
    with Image.open(test_image_path).convert("RGB") as img:
        return np.asarray(img, dtype=np.uint8)


@pytest.fixture()
def random_image_arr() -> ArrayLike:
    """Return array containing data about a random image."""
    return np.random.randint(0, 255, size=(8, 8, 3), dtype=np.uint8)


@pytest.fixture()
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
