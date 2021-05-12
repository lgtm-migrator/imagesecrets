"""Test the image_util module."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from image_secrets.backend.util import image


@pytest.mark.parametrize(
    "bytes_",
    [b"", b"qwerty", b"123456789", b"~!@#$%^&**()", b"   <>   "],
)
def test_read_bytes(bytes_: bytes) -> None:
    """Test the read_image_bytes function.

    :param bytes_: Bytes to read

    """
    num = np.random.randint(0, 10)
    assert image.read_bytes(bytes_).read(num) == bytes_[:num]


def test_data(test_image_path: Path) -> None:
    """Test the image_data function."""
    shape, arr = image.data(test_image_path)

    assert arr.ndim == 3
    assert arr.dtype == np.uint8
    assert np.logical_and(arr >= 0, arr <= 255).all()

    assert shape[-1] == 3


def test_save(tmpdir, random_image_arr) -> None:
    """Test the save function."""
    tmp_dir = tmpdir.mkdir("tmp/")
    image_fp = Path(tmp_dir / "tmp.png")

    assert not image_fp.is_file()
    image.save_array(random_image_arr, image_fp)
    assert Path(image_fp).is_file()
