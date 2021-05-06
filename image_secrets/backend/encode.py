"""Module with functions to encode text into images."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Iterator

import numpy as np

from image_secrets.backend import util
from image_secrets.settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


def encode_message(
    shape: tuple[int, int, int],
    data: ArrayLike,
    binary_message: Iterator[Iterator[str]],
    message_len: int,
) -> ArrayLike:
    """Encode a message into the source image.

    :param shape: What should the shape of the final array be like
    :param data: The flattened array with the pixel values
    :param binary_message: The string containing all of the bits to encode
    :param message_len: Length of the message to encode

    :raises ValueError: If the image array is not large enough for the message

    """
    if data.size < message_len:
        raise ValueError(
            f"The message size {message_len:,1f} is too long for the given image {data.size:,1f}.",
        )

    # __len__ of each message element is equal to the number of least significant bits to use
    lsb_n = sum(1 for _ in util.peek_next_elem(binary_message))

    data.flatten()
    for index, bit in enumerate(binary_message):
        data[index] = int(format(data[index], "08b")[:-lsb_n] + "".join(bit), base=2)

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
    """Encoding function to be used by the corresponding API endpoint.

    :param message: Message to encode
    :param file: Source image
    :param delimeter: Message delimeter
    :param lsb_n: Number of lsb to use
    :param reverse: Reverse encoding bool

    """
    b_msg = tuple(util.str_to_binary(message + delimeter))
    length = len(b_msg) // lsb_n

    shape, arr = util.image_data(file)
    if reverse:
        b_msg = reversed(b_msg)
        np.flip(arr)

    b_msg = util.flat_iterable(b_msg)
    b_msg = util.split_iterable(b_msg, lsb_n)

    enc_arr = encode_message(shape, arr, binary_message=b_msg, message_len=length)
    return enc_arr if not reverse else np.flip(enc_arr)


def cli_encode():
    ...
