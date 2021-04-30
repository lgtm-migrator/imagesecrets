"""Module with functions to encode text into images."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from PIL import Image

from image_secrets.backend import util
from image_secrets.backend.settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import ArrayLike, DTypeLike


def encode_message(
    shape: tuple[int, int, int],
    data: DTypeLike,
    binary_message: str,
) -> ArrayLike:
    """Encode a message into the source image.

    :param shape: What should the shape of the final array be like
    :param data: The flattened array with the pixel values
    :param binary_message: The string containing all of the bits to encode

    :raises ValueError: If the image array is not large enough for the message

    """
    if data.size < len(binary_message):
        raise ValueError(
            f"The message size ({len(binary_message)}) is too long for the given image ({data.size}.",
        )

    for index, bit in enumerate(binary_message):
        data[index] = int(format(data[index], "08b")[:-1] + bit, base=2)

    encoded_arr = np.array(data).reshape(shape)
    return encoded_arr


def encoded_image_name(file: Path) -> Path:
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


def main(file: str, message: str, inplace: bool = False) -> str:
    """Main encoding function.

    :param file: Path to the source file
    :param message: The message to encode
    :param inplace: Whether the message should be encoded into the given image
        or if a copy of the image should be created, defaults to False

    """
    file = Path(file.strip()).absolute()

    binary_message = util.str_to_binary(message + MESSAGE_DELIMETER)
    shape, data = util.image_data(file)
    arr = encode_message(shape, data, binary_message)

    if not inplace:
        file = encoded_image_name(file)

    save_image(arr, file)
    return file.name
