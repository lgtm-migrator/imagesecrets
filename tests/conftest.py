"""Session wide fixtures."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from image_secrets.api.config import Settings
from image_secrets.api.interface import app

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


@pytest.fixture()
def api_client() -> TestClient:
    """Return the starlette testing client."""
    return TestClient(app)


@pytest.fixture()
def api_name() -> str:
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
