"""Module with functions to encode text into images."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Iterator

import numpy as np
from PIL import Image

from image_secrets.backend import util
from image_secrets.settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


def encode_message(
    shape: tuple[int, int, int],
    data: ArrayLike,
    binary_message: str,
) -> ArrayLike:
    """Encode a message into the source image.

    :param shape: What should the shape of the final array be like
    :param data: The flattened array with the pixel values
    :param binary_message: The string containing all of the bits to encode

    :raises ValueError: If the image array is not large enough for the message

    """
    if data.size < (length := len(binary_message)):
        raise ValueError(
            f"The message size {length:,1f} is too long for the given image {data.size:,1f}.",
        )

    data = data.flatten()
    for index, bit in enumerate(binary_message):
        data[index] = int(format(data[index], "08b")[:-1] + bit, base=2)

    return data.reshape(shape)


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


def api_encode(
    message: str,
    file: Path,
    delimeter: str,
    lsb_n: int,
    reverse: bool,
) -> ArrayLike:
    """Encode."""
    b_msg = util.str_to_binary(message + delimeter)
    if lsb_n != 1:
        b_msg = "".join(util.split_seq(tuple(b_msg), lsb_n))

    shape, arr = util.image_data(file)
    if reverse:
        b_msg, arr = util.reverse_data(b_msg, arr)

    enc_arr = encode_message(shape, arr, b_msg)
    return enc_arr if not reverse else np.flip(enc_arr)


def cli_encode():
    ...
