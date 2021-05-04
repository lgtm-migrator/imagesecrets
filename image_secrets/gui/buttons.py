"""Connect buttons to the corresponding functionality."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pyperclip

from image_secrets.gui.settings import DARK_STYLESHEET, LIGHT_STYLESHEET

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow


def setup(parent: QMainWindow) -> None:
    """Connect both push buttons and menu bar actions.

    :param parent: The interface of both actions and push buttons.

    """
    push_buttons(parent)
    actions(parent)


def actions(parent: QMainWindow) -> None:
    """Connect menu bar actions with their corresponding functions or events.

    :param parent: The parent class of the interface of the actions

    """
    ui = parent.ui

    # menu general
    ui.action_home.triggered.connect(lambda: ui.stacked_widget.setCurrentIndex(0))
    ui.action_encode.triggered.connect(lambda: ui.stacked_widget.setCurrentIndex(1))
    ui.action_decode.triggered.connect(lambda: ui.stacked_widget.setCurrentIndex(2))
    ui.action_exit.triggered.connect(lambda: parent.main_win.close())

    # menu theme
    ui.action_light.triggered.connect(
        lambda: parent.main_win.setStyleSheet(LIGHT_STYLESHEET),
    )
    ui.action_dark.triggered.connect(
        lambda: parent.main_win.setStyleSheet(DARK_STYLESHEET),
    )


def push_buttons(parent: QMainWindow) -> None:
    """Connect push buttons to their corresponding functions or events.

    :param parent: The parent class of the interface of the actions

    """
    ui = parent.ui

    # home
    ui.encode_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(1))
    ui.decode_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(2))

    # encode
    ui.encode_image_btn.clicked.connect(parent.events.encode_file_dialog)
    ui.encode_submit_btn.clicked.connect(parent.events.encode_submit_event)

    # decode
    ui.decode_image_btn.clicked.connect(parent.events.decode_file_dialog)
    ui.decode_submit_btn.clicked.connect(parent.events.decode_submit_event)
    ui.decode_copy_tool_btn.clicked.connect(
        lambda: pyperclip.copy(ui.decode_plain_text_edit.toPlainText()),
    )
