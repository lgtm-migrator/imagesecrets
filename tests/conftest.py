"""Session wide fixtures."""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


@pytest.fixture(scope="session")
def image_arr():
    """Return array containing data about a random image."""
    return np.random.randint(0, 255, size=(256, 3), dtype=np.uint8)


@pytest.fixture()
def delimeter_array() -> ArrayLike:
    """Return a delimeter array, string form = 'dlm'."""
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
