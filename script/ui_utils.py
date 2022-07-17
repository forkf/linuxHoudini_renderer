"""This module is utility of pyqt customized dialogs."""

from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import QUrl


class FileBrowser(QFileDialog):
    """Main class of file browser window."""

    def __init__(self, parent=None, caption=""):
        """Initialize file-browser window.

        Args:
            parent (obj): Parent object.
            caption (str): File Browser window title.
        """
        super(FileBrowser, self).__init__(parent)
        self.setGeometry(10, 10, 700, 400)
        _dir = '/opt/'
        self.get_file = self.getExistingDirectoryUrl(
            self,
            caption,
            QUrl(_dir),
        )
