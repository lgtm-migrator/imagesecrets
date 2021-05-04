"""Test that the decode widget works properly."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pyperclip
import pytest
from PyQt5.QtCore import Qt

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow
    from pytestqt.qtbot import QtBot


@pytest.mark.parametrize(
    "text",
    [
        "",
        " ",
        "\\",
        "Copy this",
        "And this" * 100,
    ],
)
def test_copy_tool_btn(qtbot: QtBot, application: QMainWindow, text: str) -> None:
    """Test that the button correctly copies text into the clipboard.

    :param qtbot: QtBot instance
    :param application: The application to test

    """
    application.ui.decode_plain_text_edit.setPlainText(text)
    qtbot.mouseClick(application.ui.decode_copy_tool_btn, Qt.LeftButton)
    assert pyperclip.paste() == text
