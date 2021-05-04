"""Test that the home widget works properly."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from PyQt5.QtCore import Qt

from image_secrets.gui.interface import ImageSecretsWindow

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow
    from pytestqt.qtbot import QtBot


@pytest.fixture()
def application(qtbot: QtBot) -> QMainWindow:
    """Return the main window."""
    test_app = ImageSecretsWindow()
    qtbot.addWidget(test_app)
    return test_app


@pytest.mark.parametrize(
    "button, index",
    [
        ("encode_btn", 1),
        ("decode_btn", 2),
    ],
)
def test_button(
    qtbot: QtBot,
    application: QMainWindow,
    button: str,
    index: int,
) -> None:
    """Test the buttons on the home widget.

    :param qtbot: QtBot instance
    :param application: The application to test
    :param button: QPushButton pointer
    :param index: The expected stacked_widget index after clicking the button

    """
    button = getattr(application.ui, button)
    qtbot.mouseClick(button, Qt.LeftButton)
    assert application.ui.stacked_widget.currentIndex() == index
