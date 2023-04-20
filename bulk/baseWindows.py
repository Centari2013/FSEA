import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from bulk.colorPresets import colors


class windowWithToolbar(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.prevPos = None

        self.setMinimumSize(QtCore.QSize(550, 400))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.setAutoFillBackground(False)

        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setEnabled(True)
        self.centralWidget.setAutoFillBackground(False)
        self.centralWidget.setObjectName("centralWidget")

        self.primaryGridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.primaryGridLayout.setContentsMargins(0, 0, 0, 0)
        self.primaryGridLayout.setSpacing(0)
        self.primaryGridLayout.setObjectName("primaryGridLayout")

        self.titlebarFrame = QtWidgets.QFrame(self.centralWidget)
        self.titlebarLayout = QtWidgets.QHBoxLayout(self.titlebarFrame)
        self.title = QtWidgets.QLabel("F-SEA Database")

        self.minimizeButton = QtWidgets.QPushButton(self.titlebarFrame)
        self.restoreButton = QtWidgets.QPushButton(self.titlebarFrame)
        self.exitButton = QtWidgets.QPushButton(self.titlebarFrame)

        self._titleBarInit()

        self.titlebarFrame.mousePressEvent = lambda event: self._toolbarClick(event)
        self.titlebarFrame.mouseMoveEvent = lambda event: self._toolbarMove(event)

        self.footerFrame = QtWidgets.QFrame(self.centralWidget)
        self.footerLayout = QtWidgets.QGridLayout(self.footerFrame)

        self.prevPos = None
        self.savedResults = None


        self.centralWidget.setLayout(self.primaryGridLayout)
        self.setCentralWidget(self.centralWidget)

    def add_titlebar_button(self, button, click_function):
        button.clicked.connect(click_function)
        button.setMinimumSize(QtCore.QSize(18, 18))
        button.setMaximumSize(QtCore.QSize(18, 18))
        button.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        button.setStyleSheet("QPushButton { color: white;\n"
                             "border-image: url(bulk/assets/%s.png);"
                             "background-color: %s;\n"
                             "border: none; }\n"
                             "QPushButton::pressed { background-color: %s; }" % (
                                 button.objectName().lower(), colors["TITLEBAR_BUTTON_COLOR"],
                                 colors["PUSH_BUTTON_PRESSED_COLOR"]))
        self.titlebarLayout.addWidget(button)

    def _titleBarInit(self):
        self.titlebarFrame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.titlebarFrame.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.titlebarFrame.setStyleSheet("background-color: {};\n"
                                         "color: white;".format(colors["FRAME_COLOR"]))
        self.titlebarFrame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.titlebarFrame.setObjectName("titlebarFrame")

        self.titlebarLayout.setContentsMargins(15, 5, -1, 5)
        self.titlebarLayout.setObjectName("titlebarLayout")

        self.title.setObjectName("title")
        self.titlebarLayout.addWidget(self.title)

        # separates buttons from QLabel
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.titlebarLayout.addItem(spacerItem)

        self.minimizeButton.setObjectName("minimize")
        self.restoreButton.setObjectName("restore")
        self.exitButton.setObjectName("exit")

        self.add_titlebar_button(self.minimizeButton, self.showMinimized)
        self.add_titlebar_button(self.restoreButton, self._minOrMax)
        self.add_titlebar_button(self.exitButton, sys.exit)

        self.primaryGridLayout.addWidget(self.titlebarFrame, 0, 0, 1 ,2)


    def initFooter(self, *widgetList):
        self.footerFrame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.footerFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.footerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.footerFrame.setObjectName("footerFrame")

        self.footerLayout.setContentsMargins(0, 0, 0, 0)
        self.footerLayout.setObjectName("footerLayout")

        col = 0
        for w in widgetList:
            self.footerLayout.addWidget(w, 0, col, Qt.AlignmentFlag.AlignCenter)
            col += 1

        self.footerLayout.addWidget(QSizeGrip(self), 0, col, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.primaryGridLayout.addWidget(self.footerFrame, 3, 1)

    def _minOrMax(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def _toolbarClick(self, event):
        if self.exitButton.underMouse():
            pass
        elif self.minimizeButton.underMouse():
            pass
        elif self.restoreButton.underMouse():
            pass
        else:
            self.prevPos = event.globalPosition().toPoint()

    def _toolbarMove(self, event):

        # ignore buttons when moving toolbar
        if self.exitButton.underMouse():
            pass
        elif self.minimizeButton.underMouse():
            pass
        elif self.restoreButton.underMouse():
            pass
        else:

            if self.isMaximized():
                self.showNormal()
                w = self.titlebarFrame.geometry().width()
                h = self.titlebarFrame.frameGeometry().height()
                self.move(QPoint(int(self.prevPos.x() - (0.2 * w)), int(self.prevPos.y() - (0.2 * h))))

            delta = QPoint(event.globalPosition().toPoint() - self.prevPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.prevPos = event.globalPosition().toPoint()
