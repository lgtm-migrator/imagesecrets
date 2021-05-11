"""Module with functions to decode text from images."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

import numpy as np

from image_secrets.backend.util import image
from image_secrets.settings import MESSAGE_DELIMITER

if TYPE_CHECKING:
    from pathlib import Path

    from _io import BytesIO
    from numpy.typing import ArrayLike


def main(
    data: Union[BytesIO, Path],
    delimiter: str = MESSAGE_DELIMITER,
    lsb_n: int = 1,
    reverse: bool = False,
) -> str:
    """Decode text from an image.

    :param data: Pixel image data which can be converted to numpy array by PIL
    :param delimiter: Message end identifier, defaults to the one in .settings
    :param lsb_n: Number of least significant bits to decode, defaults to 1
    :param reverse: Reverse decoding bool, defaults to False

    """
    _, arr = image.data(data)
    arr = prepare_array(arr, lsb_n, reverse)

    text = decode_text(arr, delimiter)
    return text


def api(
    data: bytes,
    delimiter: str,
    lsb_n: int,
    reverse: bool,
) -> str:
    """Function to be used by the corresponding decode API endpoint.

    :param data: Data of the image uploaded by user
    :param delimiter: Message end identifier
    :param lsb_n: Number of least significant bits to decode
    :param reverse: Reverse decoding bool

    """
    data = image.read_bytes(data)
    text = main(data, delimiter, lsb_n, reverse)
    return text


def prepare_array(array: ArrayLike, lsb_n: int, reverse: bool) -> ArrayLike:
    """Prepare an array into a form from which it is easy to decode text.

    :param array: The array to work with
    :param lsb_n: How many lsb to use
    :param reverse: Whether the array should be flipped or not

    """
    shape = (-1, 8)
    if reverse:
        array = np.flip(array)
    arr = np.unpackbits(array).reshape(shape)
    arr = np.packbits(arr[:, -lsb_n:])  # cut unnecessary bits and pack the rest
    return arr


def decode_text(array: ArrayLike, delimiter) -> Optional[str]:
    """Decode text from the given array.

    :param array: The array from which to decode the text
    :param delimiter: Identifier that whole message has been extracted

    :raises StopIteration: if nothing was found in the array

    """
    text = ""
    delim_len = len(delimiter)

    # iterating is faster than vectorizing 'chr' on the whole array,
    # many slow string operation are avoided
    for num in array:
        text += chr(num)
        if text.endswith(delimiter):
            return text[:-delim_len]
    else:
        raise StopIteration("No message found after scanning the whole image.")
