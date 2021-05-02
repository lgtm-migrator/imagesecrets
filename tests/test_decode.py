"""Test the module used for decoding."""
from __future__ import annotations

import itertools as it
import random
import re
import string
from typing import TYPE_CHECKING

import numpy as np
import pytest

from image_secrets.backend import decode
from image_secrets.backend.regex import CHARS_8
from image_secrets.settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


def random_word(word=None) -> str:
    """Return a random word of length 3 + MESSAGE_DELIMETER in binary format.

    :param word: Optional argument to specify from which Sequence to pick chars, defaults to None

    """
    return "".join(
        format(ord(char), "b").zfill(8)
        for char in it.chain(
            (random.choice(word if word else string.printable[:-6]) for _ in range(3)),
            MESSAGE_DELIMETER,
        )
    )


def random_image_array() -> ArrayLike:
    """Return a random array representing an image."""
    return np.random.randint(0, 255, size=(256, 3), dtype=np.uint8)


def encoded_array(word=None) -> tuple[ArrayLike, str]:
    """Return an encoded image array and the message which is encoded in it.

    :param word: Optional argument to pass into the word creation function, defaults to None

    """
    binary_word = random_word(word if word else None)
    plain = "".join(
        (
            # decode into char
            chr(int(binary, base=2))
            for binary in (
                # split into elements with length 8
                re.findall(CHARS_8, binary_word)
            )
        )
    )

    encoded_arr = np.array([i for i in binary_word], dtype=np.uint8)
    filler_arr = random_image_array()

    return np.concatenate((encoded_arr.reshape(-1, 3), filler_arr), axis=0), plain


@pytest.mark.parametrize(
    "enc_array, expected",
    [
        (encoded_array()),
        (encoded_array(" ")),
        (encoded_array("% %")),
        (encoded_array("qwerty")),
        (encoded_array("\n\n\n")),
        (encoded_array("123")),
    ],
)
def test_decode(enc_array: ArrayLike, expected: str) -> None:
    """Test the decoding function.

    :param enc_array: Array which has a message encoded in it
    :param expected: The expected result to be decoded from the array

    """
    assert decode.decode_text(enc_array) == expected[: -len(MESSAGE_DELIMETER)]


@pytest.mark.parametrize("array", [random_image_array(), random_image_array()])
def test_decode_fail(array: ArrayLike) -> None:
    """Test that the decode function raises StopIteration if it can't find any message."""
    with pytest.raises(StopIteration):
        decode.decode_text(array)


__all__ = [
    "encoded_array",
    "random_image_array",
    "random_word",
    "test_decode",
    "test_decode_fail",
]
