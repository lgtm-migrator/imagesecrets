"""Module with functions to encode text into images."""
from __future__ import annotations

import itertools as it
from typing import Optional, TYPE_CHECKING
from pathlib import Path

import numpy as np
from PIL import Image

from settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


def image_array(file: Path) -> ArrayLike:
    with Image.open(file).convert("RGB") as img:
        return np.asarray(img.getdata(), dtype=np.uint8)


def str_into_bin_array(text_: str) -> ArrayLike:
    str_len = len(text_)
    binary = iter(
        "".join(
            map(
                lambda char: bin(char)[2:],
                bytearray(text_ + MESSAGE_DELIMETER, encoding="utf-8"),
            )
        )
    )

    if str_len % 3 == 2:
        it.chain(binary, ("0",))
    elif str_len % 3 == 1:
        it.chain(binary, ("00",))

    return np.fromiter(binary, dtype=int).reshape(-1, 3)


def encoded_img_name(file: Path) -> Path:
    name = f"encoded_{file.stem}.png"
    return Path(file.parent, name)


def save_image(arr: ArrayLike, filepath: Path) -> None:
    img = Image.fromarray(arr)
    img.save(filepath)


def encode_message(arr: ArrayLike, message: str) -> ArrayLike:
    msg_arr = str_into_bin_array(message)

    if arr.size < msg_arr.size:
        raise ValueError(
            "There is not enough pixels in the image, larger one is needed."
        )

    for pixel, msg_bit in zip(arr, msg_arr):
        for index in range(0, 3):
            binary = format(pixel[index], "08b")
            binary = binary[:-1] + str(msg_bit[index])
            pixel[index] = int(binary, base=2)

    return arr


def text(file: Path, message: str, inplace: bool = False) -> Optional[str]:
    arr = image_array(file)
    new_arr = encode_message(arr, message)

    if not inplace:
        file = encoded_img_name(file)

    save_image(new_arr, file)

    return f"\nEncoded message {message!r} into {file.name!r}"


if __name__ == "__main__":

    print(
        text(
            Path(
                "F:\\Luky\\Programy\\programovani\\imagesecrets-api\\src\\cb.png"
            ).absolute(),
            "fvfvdfvv",
        )
    )
