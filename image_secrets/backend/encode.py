"""Module with functions to encode text into images."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Iterator

import numpy as np

from image_secrets.backend import util
from image_secrets.settings import API_IMAGES, MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


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


def main_(file: str, message: str, inplace: bool = False) -> str:
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


def api(
    message: str,
    file,
    delimeter: str,
    lsb_n: int,
    reverse: bool,
) -> Path:
    """Encoding function to be used by the corresponding API endpoint.

    :param message: Message to encode
    :param file: Source image
    :param delimeter: Message delimeter
    :param lsb_n: Number of lsb to use
    :param reverse: Reverse encoding bool

    """
    arr = main(message, util.read_coroutine(file), delimeter, lsb_n, reverse)

    fp = API_IMAGES / f"{util.token_hex()}.png"
    util.save_image(arr, fp)

    return fp


def cli():
    ...


def main(
    message: str,
    file,
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
    msg_arr, msg_len = util.message_bit_array(message, delimeter, lsb_n)
    shape, img_arr, unpacked_arr = prepare_image(file, msg_len)

    if reverse:
        msg_arr, img_arr = np.flip(msg_arr), np.flip(img_arr)  # all axes get flipped

    enc_arr = encode_into_array(unpacked_arr, msg_arr)
    final_arr = merge_into_image_array(enc_arr, img_arr, shape)

    return final_arr if not reverse else np.flip(final_arr)


def prepare_image(
    file: Path,
    message_len: int,
) -> tuple[tuple[int, int, int], ArrayLike, ArrayLike]:
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

    return shape, arr[message_len:], unpacked_arr.reshape(-1, 8)


def encode_into_array(main: ArrayLike, new: ArrayLike) -> ArrayLike:
    """Encode an array into the parent array.

    :param main: The main array, encoding will happen here
    :param new: The new data to encode, will be put into the main array

    """
    lsb_n = new.shape[1]
    main[:, -lsb_n:] = new
    return main


def merge_into_image_array(
    packed: ArrayLike,
    main: ArrayLike,
    final_shape: tuple,
) -> ArrayLike:
    """concatenate two arrays into the final one.

    :param packed: The packed array with the encoded data
    :param main: Main array with the pixel data
    :param final_shape: Shape of the original image array

    """
    packed_arr = np.packbits(packed)
    final = np.concatenate((packed_arr, main))
    return final.reshape(final_shape)
