"""Module with functions to encode text into images."""
from __future__ import annotations

import itertools as it
from typing import Optional, TYPE_CHECKING
from pathlib import Path

import numpy as np
from PIL import Image

from src.backend.settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


def image_array(file: Path) -> ArrayLike:
    """Return numpy array of the given image.

    :param file: The path to the image from which to extract the data

    """
    with Image.open(file).convert("RGB") as img:
        return np.asarray(img.getdata(), dtype=np.uint8)


def str_into_bin_array(text_: str) -> ArrayLike:
    """Return numpy array of the given text.

    The text is joined with the MESSAGE_DELIMETER.
    Three columns are create so later encryption into pixels is easy.
    Extra bits are added to the text so it fits into the three columns

    :param text_: The text to turn into the binary array

    """
    # times 8 because we need binary amount
    # no need to add the delimeter here because it's divisible by 3 without any reminder
    str_len = len(text_ * 8)
    binary = iter(
        "".join(
            map(
                lambda char: format(char, "b").zfill(8),
                bytearray(text_ + MESSAGE_DELIMETER, encoding="utf-8"),
            )
        )
    )

    if str_len % 3 == 2:
        binary = it.chain(binary, "0")
    elif str_len % 3 == 1:
        binary = it.chain(binary, "00")

    return np.fromiter(binary, dtype=int).reshape(-1, 3)


def encode_message(arr: ArrayLike, message: str) -> ArrayLike:
    """Encode a message into given array.

    :param arr: The array of pixels
    :param message: The message to encode

    :raises ValueError: If the image array is not large enough for the message

    """
    msg_arr = str_into_bin_array(message)

    if arr.size < msg_arr.size:
        raise ValueError(
            f"The message (size: {msg_arr.size}) is too long for the given image (size: {arr.size}."
        )

    for pixel, msg_bit in zip(arr, msg_arr):
        for index in range(0, 3):
            binary = format(pixel[index], "08b")
            # encode into the least significant bit
            binary = binary[:-1] + str(msg_bit[index])
            pixel[index] = int(binary, base=2)

    return arr


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
    img = Image.fromarray(arr)
    img.save(filepath)


def main(file: Path, message: str, inplace: bool = False) -> Optional[str]:
    """Main encoding function.

    :param file: Path to the source file
    :param message: The message to encode
    :param inplace: Whether the message should be encoded into the given image
        or if a copy of the image should be created, defaults to False

    """
    arr = image_array(file)
    new_arr = encode_message(arr, message)

    if not inplace:
        file = encoded_img_name(file)

    save_image(new_arr, file)
    return f"\nEncoded message {message!r} into {file.name!r}"
