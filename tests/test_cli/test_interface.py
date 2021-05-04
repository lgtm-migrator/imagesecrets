"""Test the interface module."""
from __future__ import annotations

from typing import TYPE_CHECKING

from image_secrets.cli.interface import image_secrets

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_main(runner: CliRunner) -> None:
    result = runner.invoke(image_secrets)
    assert not result.exception


def test_encode(runner: CliRunner) -> None:
    result = runner.invoke(image_secrets, ["encode", "--help"])
    assert "inplace" in result.stdout


def test_encode_file(runner: CliRunner) -> None:
    result = runner.invoke(image_secrets, ["encode", "--filename", "image.png"])
    assert "Path 'image.png' does not exist." in result.stdout

    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write("testing...")

        result = runner.invoke(image_secrets, ["encode", "--filename", "test.txt"])
        assert "is not a .PNG image." in result.stdout


def test_decode(runner: CliRunner) -> None:
    result = runner.invoke(image_secrets, ["decode", "--help"])
    assert "Decode a message from <file>." in result.stdout


def test_decode_file(runner: CliRunner) -> None:
    result = runner.invoke(image_secrets, ["decode", "--filename", "image.png"])
    assert "Path 'image.png' does not exist." in result.stdout

    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write("testing...")

        result = runner.invoke(image_secrets, ["decode", "--filename", "test.txt"])
        assert "is not a .PNG image." in result.stdout


__all__ = [
    "test_decode",
    "test_decode_file",
    "test_encode",
    "test_encode_file",
    "test_main",
]
