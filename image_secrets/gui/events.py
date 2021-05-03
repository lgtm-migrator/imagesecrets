"""The main logic behind events happening on the GUI."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow


class ImageSecretsEvents:
    """Events for the ImageSecrets GUI client."""

    def __init__(self, parent: QMainWindow) -> None:
        """Construct the class."""
        self.parent = parent

    def __repr__(self) -> str:
        """Provide information about this class."""
        return f"{self.__class__.__qualname__}({self.parent})"

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

    ##########
    # Encode #
    ##########

    def encode_file_dialog(self) -> None:
        """File dialog for the image to encode."""
        if f := self.file_dialog("encode"):
            self.parent.ui.encode_pixmap_lbl.setPixmap(QPixmap(f))

    ##########
    # Decode #
    ##########

    def decode_file_dialog(self) -> None:
        """File dialog for the image to decode."""
        if f := self.file_dialog("decode"):
            self.parent.ui.decode_pixmap_lbl.setPixmap(QPixmap(f))
