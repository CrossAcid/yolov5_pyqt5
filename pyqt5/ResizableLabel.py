from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

# 自由缩放图片大小的QLable
class ResizableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(QtCore.QSize(200, 0))
        self.setStyleSheet("border:1px solid #CCCCCC;""border-radius:10px;")
        self.pixmap = None

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        super().setPixmap(pixmap)
        self._update_pixmap()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_pixmap()

    def _update_pixmap(self):
        if self.pixmap:
            size = self.size()
            scaled_pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            super().setPixmap(scaled_pixmap)