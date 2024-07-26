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

    def setPixmap(self, pixmap, flag=0):
        self.pixmap = pixmap
        super().setPixmap(pixmap)
        self._update_pixmap(flag)

    def resizeEvent(self, event, flag=0):
        super().resizeEvent(event)
        self._update_pixmap(flag)

    def _update_pixmap(self, flag=0):
        if self.pixmap:
            size = self.size()
            if ~flag:
                scaled_pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                super().setPixmap(scaled_pixmap)
            else:
                scaled_pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio)
                super().setPixmap(scaled_pixmap)
