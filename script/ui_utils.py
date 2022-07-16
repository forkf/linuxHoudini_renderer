try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except ImportError:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *


class FileBrowser(QFileDialog):
    def __init__(self, parent=None, caption=""):
        super(FileBrowser, self).__init__(parent)
        self.setGeometry(10, 10, 700, 400)
        _dir = '/opt/'
        self.get_file = self.getExistingDirectoryUrl(
            self,
            caption,
            QUrl(_dir),
        )
