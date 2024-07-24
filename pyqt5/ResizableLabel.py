from PyQt5 import Qt
from PyQt5.QtWidgets import QLabel


class ResizableLabel(QLabel):
    def __init__(self, parent=None):
        super(ResizableLabel, self).__init__(parent)
        self.pixmap = None

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        super().setPixmap(self.pixmap)

    def resizeEvent(self, event):
        if self.pixmap:
            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            super().setPixmap(scaled_pixmap)
        super(ResizableLabel, self).resizeEvent(event)