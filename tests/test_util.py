"""Test the util module."""
from __future__ import annotations

import functools as fn
from typing import TYPE_CHECKING

import numpy as np
import pytest

from image_secrets.backend import util

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


np.array = fn.partial(np.array, dtype=np.uint8)


@pytest.mark.parametrize(
    "message, bits, expected_arr",
    [
        (" ", 1, np.array(([0], [0], [1], [0], [0], [0], [0], [0]))),
        ("A", 1, np.array(([0], [1], [0], [0], [0], [0], [0], [1]))),
        ("1", 1, np.array(([0], [0], [1], [1], [0], [0], [0], [1]))),
        ("22", 2, np.array(([0], [0], [1], [1], [0], [0], [1], [0]) * 2)),
        ("333", 3, np.array(([0], [0], [1], [1], [0], [0], [1], [1]) * 3)),
        ("4444", 4, np.array(([0], [0], [1], [1], [0], [1], [0], [0]) * 4)),
        ("55555", 5, np.array(([0], [0], [1], [1], [0], [1], [0], [1]) * 5)),
        ("666666", 6, np.array(([0], [0], [1], [1], [0], [1], [1], [0]) * 6)),
        ("7777777", 7, np.array(([0], [0], [1], [1], [0], [1], [1], [1]) * 7)),
        ("88888888", 8, np.array(([0], [0], [1], [1], [1], [0], [0], [0]) * 8)),
        ("Z" * 50, 1, np.array(([0], [1], [0], [1], [1], [0], [1], [0]) * 50)),
        ("&" * 50, 5, np.array(([0], [0], [1], [0], [0], [1], [1], [0]) * 50)),
    ],
)
def test_message_bit_array(
    message: str,
    bits: int,
    expected_arr: ArrayLike,
    delimeter_array,
) -> None:
    """Test the prepare message function."""
    expected_arr = np.concatenate((expected_arr, delimeter_array))
    expected_arr.resize(
        (np.ceil(expected_arr.size / bits).astype(int), bits),
        refcheck=False,
    )

    array, length = util.message_bit_array(message, "dlm", bits)

    # numpy testing for better visual array differences, raises AssertionError same way like assert
    np.testing.assert_array_equal(array, expected_arr)
    assert length == expected_arr.size // bits


__all__ = [
    "test_message_bit_array",
]
