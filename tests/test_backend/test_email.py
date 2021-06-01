"""Test the email module."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest
from pydantic import EmailStr

from image_secrets.api.dependencies import get_mail
from image_secrets.backend import email

if TYPE_CHECKING:
    from email.mime.multipart import MIMEMultipart

    from fastapi_login import FastMail

loop = asyncio.get_event_loop()


@pytest.fixture(scope="module")
def client() -> FastMail:
    """Return email client in a test mode."""
    mail_client = get_mail()
    mail_client.config.SUPPRESS_SEND = 1
    mail_client.config.USE_CREDENTIALS = False
    return mail_client


@pytest.mark.parametrize(
    "recipient, username",
    [("email@example.com", "test_username"), ("email@test.abc", "abc")],
)
def test_send_welcome(client: FastMail, recipient: str, username: str) -> None:
    """Test the send_welcome function."""
    coro = email.send_welcome(
        client=client,
        recipient=EmailStr(recipient),
        username=username,
    )
    with client.record_messages() as outbox:
        loop.run_until_complete(coro)

        assert len(outbox) == 1
        out: MIMEMultipart = outbox[0]

    assert out["From"] == "string@example.com"
    assert out["To"] == recipient
    assert out["Subject"] == "Welcome to ImageSecrets"
    assert not out.defects
