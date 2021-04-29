"""Module with functions to encode text into images."""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from pathlib import Path

import numpy as np
from PIL import Image

from src.backend.settings import MESSAGE_DELIMETER
from src.backend import util

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


def encode_message(file: Path, message: str) -> ArrayLike:
    """Encode a message into given array.

    :param file: Path to the source image
    :param message: The message to encode

    :raises ValueError: If the image array is not large enough for the message

    """
    binary_msg = util.str_to_binary(message + MESSAGE_DELIMETER)
    shape, data = util.image_data(Path(file).absolute())

    if data.size < len(binary_msg):
        raise ValueError(
            f"The message (size: {len(binary_msg)}) is too long for the given image (size: {data.size}."
        )

    for index, bit in enumerate(binary_msg):
        data[index] = int(format(data[index], "08b")[:-1] + bit, base=2)

    encoded_arr = np.array(data).reshape(shape)
    return encoded_arr


def encoded_img_name(file: Path) -> Path:
    """Return a new filename with the 'encoded_ prefix'.

    :param file: The filepath to the image

    """
    name = f"encoded_{file.stem}.png"
    return Path(file.parent, name)


def save_image(arr: ArrayLike, filepath: Path) -> None:
    """Save a new image.

    :param arr: The numpy array with the pixel data
    :param filepath: The path where the image should be saved

    """
    Image.fromarray(np.uint8(arr)).convert("RGB").save(filepath)


def main(file: Path, message: str, inplace: bool = False) -> Optional[str]:
    """Main encoding function.

    :param file: Path to the source file
    :param message: The message to encode
    :param inplace: Whether the message should be encoded into the given image
        or if a copy of the image should be created, defaults to False

    """
    arr = encode_message(file, message)

    if not inplace:
        file = encoded_img_name(file)

    save_image(arr, file)
    return f"Encoded message {message!r} into {file.name!r}"
