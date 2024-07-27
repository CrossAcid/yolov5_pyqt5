import sys

# 去除警告
import warnings

from PyQt5 import QtCore
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QCoreApplication, QRect, QPoint

from pyqt5.ResizableLabel import ResizableLabel
from pyqt5.utils.utils import get_real_resolution
from pyqt5.yoloThread import yoloThread

warnings.filterwarnings("ignore", category=DeprecationWarning)

from mainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self._startPos = None
        self._isTracking = None
        self._endPos = None

        # 设置无边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setupUi(self)

        self.maxAsideWidth = self.frame_left_aside.maximumWidth()
        self.minAsideWidth = self.frame_left_aside.minimumWidth()

        # 绑定按钮事件
        # 1.窗口按钮
        self.pushButton_close.clicked.connect(self.queryExit)
        self.pushButton_normal.clicked.connect(self.minimizedOrNormal)
        self.pushButton_minimize.clicked.connect(self.showMinimized)
        # 2.文件选择按钮
        self.pushButton_image.clicked.connect(self.inputImage)
        # 3.检测按钮
        self.pushButton_play.clicked.connect(self.runOrContinue)

        # QSplitter实现图片自由缩放
        self.label_origin = ResizableLabel(self.splitter)
        self.label_detect = ResizableLabel(self.splitter)

        self.yoloThread = yoloThread()
        self.yoloThread.send_msg.connect(lambda x: self.showMsg(x))
        self.yoloThread.send_result.connect(lambda x: self.load_images(x, 1))

        self.imgPath = ''

    def load_images(self, fileName, types=0):
        if types:
            print("11111")
            print(fileName)
            print("./result" + fileName)
            pixmap = QPixmap("./result/" + fileName)
            print(pixmap)
            self.label_detect.setPixmap(pixmap)
        else:
            pixmap = QPixmap(fileName)
            self.label_origin.setPixmap(pixmap)

    # 关闭窗口
    def queryExit(self):
        res = QMessageBox.question(self, "Warning", "Quit?", QMessageBox.Yes | QMessageBox.Cancel)
        if res == QMessageBox.Yes:
            QCoreApplication.instance().exit()

    # 最小化或放大窗口
    def minimizedOrNormal(self):
        if self.isMaximized():
            # 修改窗口大小
            self.showNormal()
            self.resize(1440, 810)
            self.frame_main.setGeometry(QRect(0, 0, 1440, 810))
            # 修改图标
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icon/icon/square.png"), QIcon.Normal, QIcon.Off)
            self.pushButton_normal.setIcon(icon)
            # 修改QSplitter大小从而优化感官
            self.frame_left_aside.setMinimumWidth(self.minAsideWidth)
            self.splitter.setMinimumSize(QtCore.QSize(0, 0))
        else:
            # 自定义函数动态获取屏幕分辨率
            # 修改窗口大小
            width, height = get_real_resolution()
            self.resize(width, height)
            self.frame_main.setGeometry(QRect(0, 0, width, height))
            self.showMaximized()
            # 修改图标
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icon/icon/minimize_2.png"), QIcon.Normal, QIcon.Off)
            self.pushButton_normal.setIcon(icon)
            # 修改QSplitter大小从而优化感官
            self.frame_left_aside.setMinimumWidth(self.maxAsideWidth)
            self.splitter.setMinimumSize(QtCore.QSize(width - self.frame_left_aside.minimumWidth() - 30, 0))

    # 鼠标移动事件
    def mouseMoveEvent(self, a0: QMouseEvent):
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            # 移动窗口
            self.move(self.pos() + self._endPos)

    # 鼠标按下事件
    def mousePressEvent(self, a0: QMouseEvent):
        # 根据鼠标按下时的位置判断是否在QFrame范围内
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "frame_title":
            # 判断鼠标按下的是左键
            if a0.button() == Qt.LeftButton:
                self._isTracking = True
                # 记录初始位置
                self._startPos = QPoint(a0.x(), a0.y())

    # 鼠标松开事件
    def mouseReleaseEvent(self, a0: QMouseEvent):
        if a0.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, a0: QMouseEvent):
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "frame_title":
            if a0.button() == Qt.LeftButton:
                self.minimizedOrNormal()

    def inputImage(self):
        print("button clicked")
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "JPG Files (*.jpg);;PNG Files (*.png)")
        self.load_images(file_path)
        self.imgPath = file_path

    def showMsg(self, message):
        self.statusBar.showMessage("  " + message)

    def runOrContinue(self):
        if self.imgPath != '':
            self.yoloThread.run(source=self.imgPath)
        else:
            self.showMsg('未选择图片或视频')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
