import re
from pathlib import Path

import click

from src.backend import encode as enc
from src.backend import decode as dec
from src.backend.util import validate_png


@click.group()
@click.pass_context
def cli(ctx):
    """CLI tool used for encoding and decoding messages into/from images."""


@cli.command()
@click.option(
    "--filename",
    type=click.Path(exists=True, resolve_path=True),
    prompt=True,
    callback=validate_png,
)
@click.option("--message", "text", type=str, prompt=True)
@click.option("--inplace", type=bool, default=False, show_default=True)
def encode(filename: str, text: str, inplace: bool):
    """Encode image command.

    :param filename: The filename of the source image, must have a .png extension
    :param text: The text to encode
    :param inplace: Whether the message should be encoded into the given image
        or if a copy of the image should be created, defaults to False

    """
    try:
        click.echo(f"\n{enc.main(Path(filename).absolute(), text, inplace)}")
    except ValueError as e:
        click.echo(e)


@cli.command()
@click.option("--filename", type=click.Path(exists=True), prompt=True)
def decode(filename):
    """Decode image"""
    click.echo(dec.main(filename))


if __name__ == "__main__":
    cli()
