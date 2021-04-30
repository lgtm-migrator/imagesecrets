"""Test the module used for decoding."""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

from image_secrets.backend import decode, encode

if TYPE_CHECKING:
    from numpy.typing import DTypeLike


@pytest.fixture()
def flat_array() -> DTypeLike:
    ...
