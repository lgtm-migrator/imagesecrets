"""Utility functions for cli."""
from pathlib import Path
from typing import Optional

import click


def validate_png(_, file: str) -> Optional[str]:
    """Validate that the file has a png extension.

    :param _: Dump the context passed in by click
    :param file: The file to check

    :raises BadParameter: If the pattern does not match

    """
    fp = Path(file)
    if fp.suffix.casefold() == ".png":
        return file
    raise click.BadParameter(f"The file {file!s} is not a .PNG image.")


__all__ = [
    "validate_png",
]
