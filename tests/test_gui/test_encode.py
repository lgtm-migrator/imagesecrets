"""Test that the encode widget workks properly."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from image_secrets.gui.interface import ImageSecretsWindow

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow
    from pytestqt.qtbot import QtBot


@pytest.fixture()
def application(qtbot) -> QMainWindow:
    """Return the main window."""
    test_app = ImageSecretsWindow()
    qtbot.addWidget(test_app)
    return test_app


def test_submit_button(qtbot: QtBot, application: QMainWindow) -> None:
    """Test the encode_image_btn.

    :param qtbot: QtBot instance
    :param application: The application to test

    """
    btn = getattr(application.ui, "encode_submit_btn")
