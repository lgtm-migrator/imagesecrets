from pathlib import Path

import click

from backend.image import Image


@click.group()
@click.pass_context
def cli(ctx):
    """CLI tool used for encoding and decoding messages from images."""


@cli.command()
@click.option("--filename", type=click.Path(exists=True), prompt=True)
@click.option("--message", type=str, prompt=True)
def encode(filename: str, message: str):
    """Encode image"""
    click.echo(Image(Path(filename)).encode(message))


@cli.command()
@click.option("--filename", type=click.Path(exists=True), prompt=True)
def decode(filename):
    """Decode image"""
    click.echo(Image(filename).decode())


if __name__ == "__main__":
    cli()
