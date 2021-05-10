"""Module with functions to encode text into images."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Union

import numpy as np

from image_secrets.backend import util
from image_secrets.settings import API_IMAGES, MESSAGE_DELIMETER

if TYPE_CHECKING:
    from _io import BytesIO
    from numpy.typing import ArrayLike


def main(
    message: str,
    data: Union[BytesIO, Path],
    delimeter: str = MESSAGE_DELIMETER,
    lsb_n: int = 1,
    reverse: bool = False,
) -> ArrayLike:
    """Main encoding interface.

    :param message: Message to encode
    :param data: Pixel image data which can be converted to numpy array by PIL
    :param delimeter: Message end identifier, defaults to the one in .settings
    :param lsb_n: Number of least significant bits to decode, defaults to 1
    :param reverse: Reverse decoding bool, defaults to False

    """
    msg_arr, msg_len = util.message_bit_array(message, delimeter, lsb_n)
    shape, img_arr, unpacked_arr = prepare_image(data, msg_len)

    if reverse:
        msg_arr, img_arr = np.flip(msg_arr), np.flip(img_arr)  # all axes get flipped

    enc_arr = encode_into_bit_array(unpacked_arr, msg_arr)
    final_arr = merge_into_image_array(enc_arr, img_arr, shape)

    return final_arr if not reverse else np.flip(final_arr)


def api(
    message: str,
    file: bytes,
    delimeter: str,
    lsb_n: int,
    reverse: bool,
) -> Path:
    """Encode interface for the corresponding API endpoint.

    :param message: Message to encode
    :param file: Data of the image uploaded by user
    :param delimeter: Message end identifier
    :param lsb_n: Number of least significant bits to use
    :param reverse: Reverse encoding bool

    """
    data = util.read_coroutine(file)
    arr = main(message, data, delimeter, lsb_n, reverse)

    fp = API_IMAGES / f"{util.token_hex()}.png"
    util.save_image(arr, fp)

    return fp


def cli():
    ...


def prepare_image(
    data: Union[BytesIO, Path],
    message_len: int,
) -> tuple[tuple[int, int, int], ArrayLike, ArrayLike]:
    """Prepare an image for encoding.

    :param data: Pixel image data which can be converted to numpy array by PIL
    :param message_len: Length of the message which will be encoded

    """
    shape, arr = util.image_data(data)

    arr = arr.ravel()
    unpacked_arr = np.unpackbits(
        # unpack only needed ones, instead of millions
        arr[:message_len],
    )

    return shape, arr[message_len:], unpacked_arr.reshape(-1, 8)


def encode_into_bit_array(base: ArrayLike, new: ArrayLike) -> ArrayLike:
    """Encode an array into the parent array.

    :param base: The main array, data will be encoded into here
    :param new: The new data to encode, will be put into the base array

    """
    lsb_n = new.shape[1]
    base[:, -lsb_n:] = new
    return main


def merge_into_image_array(
    packed: ArrayLike,
    main: ArrayLike,
    final_shape: tuple,
) -> ArrayLike:
    """Concatenate two arrays into the final one.

    :param packed: The packed array with the encoded data
    :param main: Main array with the pixel data
    :param final_shape: Shape of the original image array

    """
    packed_arr = np.packbits(packed)
    final = np.concatenate((packed_arr, main))
    return final.reshape(final_shape)


__all__ = [
    "api",
    "cli",
    "encode_into_bit_array",
    "main",
    "merge_into_image_array",
    "prepare_image",
]
