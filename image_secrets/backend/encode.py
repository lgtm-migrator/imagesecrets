"""Module with functions to encode text into images."""
from __future__ import annotations

import math
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Optional

import numpy as np

from image_secrets.backend import util
from image_secrets.settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import DTypeLike


def encode_message(
    data: DTypeLike,
    binary_message: Iterator[Iterator[str]],
    message_len: int,
    lsb_n: int,
) -> DTypeLike:
    """Encode a message into the source image.

    :param data: The flattened array with the pixel values
    :param binary_message: The string containing all of the bits to encode
    :param message_len: Length of the message to encode
    :param lsb_n: ...

    :raises ValueError: If the image array is not large enough for the message

    """
    if data.size < message_len:
        raise ValueError(
            f"The message size {message_len:,1f} is too long for the given image ({data.size:,1f}).",
        )

    for index, bit in enumerate(binary_message):
        data[index] = int(format(data[index], "08b")[:-lsb_n] + "".join(bit), base=2)

    return data


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
) -> DTypeLike:
    """Encoding function to be used by the corresponding API endpoint.

    :param message: Message to encode
    :param file: Source image
    :param delimeter: Message delimeter
    :param lsb_n: Number of lsb to use
    :param reverse: Reverse encoding bool

    """
    b_msg = tuple(util.str_to_binary(message + delimeter))
    length = math.ceil(len(b_msg) / lsb_n)

    shape, arr = util.image_data(file)
    if reverse:
        b_msg = reversed(b_msg)
        np.flip(arr)

    b_msg = util.flat_iterable(b_msg)
    b_msg = util.split_iterable(b_msg, lsb_n)

    enc_arr = encode_message(arr.flatten(), b_msg, length, lsb_n)
    enc_arr.reshape(shape)

    return enc_arr if not reverse else np.flip(enc_arr)


def cli_encode():
    ...


def api_encode__Sub(
    message: str,
    file: Path,
    delimeter: str,
    lsb_n: int,
    reverse: bool,
) -> DTypeLike:
    """Encoding function to be used by the corresponding API endpoint.

    :param message: Message to encode
    :param file: Source image
    :param delimeter: Message delimeter
    :param lsb_n: Number of lsb to use
    :param reverse: Reverse encoding bool

    """
    msg_arr, msg_len = prepare_message(message, delimeter, lsb_n)
    shape, img_arr, parent_arr = prepare_image(file, msg_len)

    enc_arr = encode_into_image(parent_arr, msg_arr)
    final_arr = concatenate_arrays(enc_arr, parent_arr[msg_len:], shape)

    util.save_image(final_arr, util.encoded_image_name(file))


def prepare_message(message: str, delimeter: str, bits: int) -> tuple[DTypeLike, int]:
    """Prepare a message for encoding.

    :param message: Main message to encode
    :param delimeter: Message end identifier
    :param bits: Amount of bits per pixel

    """
    message = (message + delimeter).encode("utf-8")

    msg_arr = np.frombuffer(message, dtype=np.uint8)
    lsbits_arr = np.unpackbits(msg_arr).reshape((-1, bits))
    msg_len, _ = lsbits_arr.shape

    return lsbits_arr, msg_len


def prepare_image(
    file: Path,
    message_len: int,
) -> tuple[tuple[int, int, int], DTypeLike, DTypeLike]:
    """Prepare an image for encoding.

    :param file: Path to the chosen image
    :param message_len: Length of the message which will be encoded

    """
    shape, arr = util.image_data(file)

    arr = arr.ravel()
    unpacked_arr = np.unpackbits(
        # unpack only needed ones, instead of millions
        arr[:message_len],
    )

    return shape, arr, unpacked_arr.reshape(-1, 8)


def encode_into_image(main: DTypeLike, new: DTypeLike) -> DTypeLike:
    """Encode an array into the parent array.

    :param main: The main array, encoding will happen here
    :param new: The new data to encode, will be put into the main array

    """
    lsb_n = new.shape[1]
    main[:, -lsb_n:] = new
    return main


def concatenate_arrays(
    packed: DTypeLike,
    main: DTypeLike,
    final_shape: tuple,
) -> DTypeLike:
    """concatenate two arrays into the final one.

    :param packed: The packed array with the encoded data
    :param main: Main array with the pixel data
    :param final_shape: Shape of the original image array

    """
    packed_arr = np.packbits(packed)
    final = np.concatenate((packed_arr, main))
    return final.reshape(final_shape)
