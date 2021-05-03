"""The main logic behind events happening on the GUI."""
from __future__ import annotations

import contextlib
import re
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

from image_secrets.backend.decode import main as decode_main
from image_secrets.backend.encode import main as encode_main
from image_secrets.backend.regex import PNG_EXT

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton


def event_handler_factory(options: dict[str, Callable[[], None]]) -> Callable[[], None]:
    """Generate a new event handler.

    :param options: Dictionary containing keys and functions tied to them.

    """

    def handler(btn: QPushButton) -> None:
        """Handle clicks on message box window.

        :param btn: Clicked button

        """
        with contextlib.suppress(KeyError):
            event = options[btn.text()]
        with contextlib.suppress(UnboundLocalError):
            event()

    return handler


class ImageSecretsEvents:
    """Events for the ImageSecrets GUI client."""

    _working_image_path: Path

    def __init__(self, parent: QMainWindow) -> None:
        """Construct the class."""
        self.parent = parent

    def __repr__(self) -> str:
        """Provide information about this class."""
        return f"{self.__class__.__qualname__}({self.parent!r})"

    @property
    def working_image(self) -> Path:
        """Return the current working image."""
        return Path(self._working_image_path)

    @working_image.setter
    def working_image(self, new: str | Path) -> None:
        """Set a new current working image.

        :param new: The path to the new image

        """
        if not re.match(PNG_EXT, str(new)):
            raise ValueError("Only png images are supported.")
        self._working_image_path = Path(new)

    def file_dialog(self, action: str) -> str:
        """Ask the user to choose an image.

        :param action: The reason why was the file dialog called (encode/decode)

        """
        # dump used file filter
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent,
            f"ImageSecrets - Choose the image to {action.lower()}",
            str(Path.home()),
            "Image files (*.png)",
        )
        return fname

    def message_box(self, label: str) -> QMessageBox:
        """Return a partially initialized messaged box object."""
        box = QtWidgets.QMessageBox(self.parent.main_win)
        box.setWindowTitle(
            f"{self.parent.main_win.windowTitle()} - {label.capitalize()}",
        )
        return box

    ##########
    # Encode #
    ##########

    def encode_file_dialog(self) -> None:
        """File dialog for the image to encode."""
        if f := self.file_dialog("encode"):
            self.working_image = f
            self.parent.ui.encode_pixmap_lbl.setPixmap(QPixmap(f))

    def encode_submit_event(self) -> None:
        """Verify that a message can be encoded."""
        try:
            _ = self.working_image
        except AttributeError:
            box = self.message_box("encode")
            box.setText("Can't encode message when there isn't any image chosen.")
            box.setIcon(QtWidgets.QMessageBox.Warning)
            box.setInformativeText("Specify the image and try again.")
            box.exec()
        else:
            if not self.parent.ui.encode_plain_text_edit.toPlainText():
                box = self.message_box("encode")
                box.setText("There is no text to encode.")
                box.setIcon(QtWidgets.QMessageBox.Warning)
                box.setInformativeText(
                    "Enter some text into the text field and try again.",
                )
                box.exec()
            else:
                self.encode_box()

    def encode_box(self) -> None:
        """Show a message box asking for details about encoding."""
        box = self.message_box("encode")
        box.setText("Encode the message into the original image?")
        box.setIcon(QMessageBox.Question)
        box.setInformativeText(
            "Message can either be encoded into the original image"
            "or into a copy of the original image.",
        )
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDetailedText(QMessageBox.No)
        box.buttonClicked.connect(
            event_handler_factory(
                {
                    "&Yes": lambda: self.encode_message(inplace=True),
                    "&No": lambda: self.encode_message(inplace=False),
                },
            ),
        )
        box.exec()

    def encode_message(self, inplace: bool) -> None:
        """Encode message into the current image.

        :param inplace: Whether the encoding should happen in the original image or in a copy of it

        """
        try:
            encode_main(
                str(self.working_image),
                self.parent.ui.encode_plain_text_edit.toPlainText(),
                inplace,
            )
        except ValueError:
            print("message too long.")

    ##########
    # Decode #
    ##########

    def decode_file_dialog(self) -> None:
        """File dialog for the image to decode."""
        if f := self.file_dialog("decode"):
            self.working_image = f
            self.parent.ui.decode_pixmap_lbl.setPixmap(QPixmap(f))

    def decode_submit(self) -> None:
        """Decode a message from the current image."""
        try:
            self.parent.ui.decode_plain_text_edit.setPlainText(
                decode_main(str(self.working_image)),
            )
        except StopIteration:
            print("no msg")
