"""Utility functions for working with images."""
from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING, Union

import numpy as np
from PIL import Image

from image_secrets.backend.util import main
from image_secrets.settings import API_IMAGES

if TYPE_CHECKING:
    from pathlib import Path

    from _io import BytesIO as TBytesIO
    from numpy.typing import ArrayLike


def read_bytes(data_: bytes) -> TBytesIO:
    """Read and return the bytes created by ``FileUpload``.

    :param data_: The data to read

    """
    return BytesIO(data_)


def data(file: Union[TBytesIO, Path], /) -> tuple[tuple[int, int, int], ArrayLike]:
    """Return numpy array of the given image.

    :param file: The path to the image from which to extract the data

    """
    with Image.open(file).convert("RGB") as img:
        arr = np.asarray(img, dtype=np.uint8)
    return arr.shape, arr


def save_array(arr: ArrayLike, /) -> Path:
    """Save a new image.

    :param arr: The numpy array with the pixel data

    """
    filename = f"{main.token_hex(16)}.png"
    fp = API_IMAGES / filename
    Image.fromarray(np.uint8(arr)).convert("RGB").save(str(fp))
    return fp
