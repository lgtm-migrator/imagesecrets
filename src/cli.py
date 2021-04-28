from pathlib import Path

import click

from backend import message


@click.group()
@click.pass_context
def cli(ctx):
    """CLI tool used for encoding and decoding messages from images."""


@cli.command()
@click.option("--filename", type=click.Path(exists=True), prompt=True)
@click.option("--message", "text", type=str, prompt=True)
def encode(filename: str, text: str):
    """Encode image"""
    click.echo(message.encode_text(filename, text))


@cli.command()
@click.option("--filename", type=click.Path(exists=True), prompt=True)
def decode(filename):
    """Decode image"""
    click.echo(message.decode_text(filename))


if __name__ == "__main__":
    cli()
