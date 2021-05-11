"""Utility functions."""
from __future__ import annotations

import secrets
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

import numpy as np
from PIL import Image

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


_T = TypeVar("_T")


def message_bit_array(message: str, delimiter: str, bits: int) -> tuple[ArrayLike, int]:
    """Return a message turned into bits in an array.

    :param message: Main message to encode
    :param delimiter: Message end identifier
    :param bits: Amount of bits per pixel

    """
    message = (message + delimiter).encode("utf-8")

    msg_arr = np.frombuffer(message, dtype=np.uint8)
    lsbits_arr = np.unpackbits(msg_arr)
    lsbits_arr.resize(
        (np.ceil(lsbits_arr.size / bits).astype(int), bits),
        refcheck=False,
    )
    msg_len, _ = lsbits_arr.shape

    return lsbits_arr, msg_len


def read_image_bytes(data: bytes) -> BytesIO:
    """Read and return the bytes created by ``FileUpload``.

    :param data: The data to read

    """
    return BytesIO(data)


def image_data(file: Path, /) -> tuple[tuple[int, int, int], ArrayLike]:
    """Return numpy array of the given image.

    :param file: The path to the image from which to extract the data

    """
    with Image.open(file).convert("RGB") as img:
        arr = np.asarray(img, dtype=np.uint8)
    return arr.shape, arr


def save_image(arr: ArrayLike, filepath: Path, /) -> None:
    """Save a new image.

    :param arr: The numpy array with the pixel data
    :param filepath: The path where the image should be saved

    """
    Image.fromarray(np.uint8(arr)).convert("RGB").save(filepath)


def token_hex(length: int = 16) -> str:
    """Return a random token hex.

    :param length: How many chars should the final token have

    """
    return secrets.token_hex(np.ceil(abs(length) / 2).astype(int))


__all__ = [
    "image_data",
    "message_bit_array",
    "save_image",
    "token_hex",
]
