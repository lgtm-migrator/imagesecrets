"""Test the array_util module."""
from __future__ import annotations

import functools as fn
from typing import TYPE_CHECKING

import numpy as np
import pytest

from image_secrets.backend.util import array

if TYPE_CHECKING:
    from numpy.typing import ArrayLike

np.array = fn.partial(np.array, dtype=np.uint8)  # no need to repeat dtype again


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
    delimiter_array,
) -> None:
    """Test the prepare message function.

    :param message: Message to turn into bit array
    :param bits: Number of bits to use
    :param expected_arr: Expected result
    :param delimiter_array: Delimiter array fixture

    """
    expected_arr = np.concatenate((expected_arr, delimiter_array))
    expected_arr.resize(
        (np.ceil(expected_arr.size / bits).astype(int), bits),
        refcheck=False,
    )

    arr, length = array.message_bit(message, "dlm", bits)

    # numpy testing for better visual array differences, raises AssertionError same way like assert
    np.testing.assert_array_equal(arr, expected_arr)
    assert length == expected_arr.size // bits


r = fn.partial(np.random.randint, low=0, high=255, size=192, dtype=np.uint8)


@pytest.mark.parametrize(
    "new, col_num, start_from_end",
    [
        (r(), 1, True),
        (r(), 2, True),
        (r(), 3, True),
        (r(), 1, False),
        (r(), 2, False),
        (r(), 3, False),
    ],
)
def test_edit_column(
    random_image_arr: ArrayLike,
    new: ArrayLike,
    col_num: int,
    start_from_end: bool,
) -> None:
    """Test the edit column function."""
    bitlike_shape = (-1, 8)

    random_image_arr = random_image_arr.reshape(bitlike_shape)
    new = new.reshape(-1, col_num)[: random_image_arr.shape[0], :]

    if start_from_end:
        random_image_arr[:, -col_num:] = new
    else:
        random_image_arr[:, :col_num] = new

    result = array.edit_column(
        random_image_arr.reshape(bitlike_shape),
        new,
        col_num,
        start_from_end,
    )

    np.testing.assert_array_equal(result, random_image_arr)


r = np.random.randint(0, 2, size=(20, 8), dtype=np.uint8)


@pytest.mark.parametrize("unpacked", [r, r, r, r, r, r])
def test_pack_and_concatenate(random_image_arr, unpacked) -> None:
    """Test the pack and concatenate function."""

    result = array.pack_and_concatenate(
        unpacked.ravel(),
        random_image_arr.ravel(),
        (-1,),
    )

    np.testing.assert_array_equal(
        result.ravel()[: -random_image_arr.size],
        np.packbits(unpacked),
    )
