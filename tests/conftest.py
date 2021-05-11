"""Session wide fixtures."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import pytest

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


@pytest.fixture()
def test_image_path() -> Path:
    """Return the path to the test.png image."""
    return Path(__file__).parent / "test.png"


@pytest.fixture()
def random_image_arr():
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
