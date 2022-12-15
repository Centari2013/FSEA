from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class windowWithToolbar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.prevPos = None

        sizePolicy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

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
        self.titlebarFrame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.titlebarFrame.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.titlebarFrame.setStyleSheet("background-color: #31353D;\n"
                                    "color: white;")
        self.titlebarFrame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.titlebarFrame.setObjectName("titlebarFrame")
        self.primaryGridLayout.addWidget(self.titlebarFrame, 0, 0, 1, 2)

        self.titlebarLayout = QtWidgets.QHBoxLayout(self.titlebarFrame)
        self.titlebarLayout.setContentsMargins(15, 5, -1, 5)
        self.titlebarLayout.setObjectName("titlebarLayout")

        self.title = QtWidgets.QLabel("F-SEA Database")
        self.title.setObjectName("title")
        self.titlebarLayout.addWidget(self.title)

        # separates buttons from QLabel
        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                                QtWidgets.QSizePolicy.Policy.Minimum)
        self.titlebarLayout.addItem(self.spacerItem)

        self.minimizeButton = QtWidgets.QPushButton(self.titlebarFrame)
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.minimizeButton.setMinimumSize(QtCore.QSize(18, 18))
        self.minimizeButton.setMaximumSize(QtCore.QSize(18, 18))
        self.minimizeButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.minimizeButton.setStyleSheet("QPushButton { color: white;\n"
                                          "border-image: url(bulk/assets/minimize.png);"
                                          "background-color: #31353D;\n"
                                          "border: none; }\n"
                                          "QPushButton::pressed { background-color: #111314; }")

        self.minimizeButton.setObjectName("minimizeButton")
        self.titlebarLayout.addWidget(self.minimizeButton)
        self.restoreButton = QtWidgets.QPushButton(self.titlebarFrame)

        def minOrMax():
            if self.isMaximized():
                self.showNormal()
            elif not self.isMaximized():
                self.showMaximized()

        self.restoreButton.clicked.connect(minOrMax)
        self.restoreButton.setMinimumSize(QtCore.QSize(18, 18))
        self.restoreButton.setMaximumSize(QtCore.QSize(18, 18))
        self.restoreButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.restoreButton.setStyleSheet("QPushButton { color: white;\n"
                                         "border-image: url(bulk/assets/maximize.png);"
                                         "background-color: #31353D;\n"
                                         "border: none; }\n"
                                         "QPushButton::pressed { background-color: #111314; }")

        self.restoreButton.setObjectName("restoreButton")
        self.titlebarLayout.addWidget(self.restoreButton)

        self.exitButton = QtWidgets.QPushButton(self.titlebarFrame)
        self.exitButton.setMinimumSize(QtCore.QSize(18, 18))
        self.exitButton.setMaximumSize(QtCore.QSize(18, 18))
        self.exitButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.exitButton.setStyleSheet("QPushButton { color: white;\n"
                                      "background-color: #31353D;\n"
                                      "border-image: url(bulk/assets/closeButton.png); }\n"
                                      "QPushButton::pressed { background-color: #111314; }")

        self.exitButton.setObjectName("exitButton")
        self.titlebarLayout.addWidget(self.exitButton)

        self.titlebarFrame.mousePressEvent = lambda event: self.toolbarClick(event)
        self.titlebarFrame.mouseMoveEvent = lambda event: self.toolbarMove(event)

        self.prevPos = None
        self.savedResults = None

    def toolbarClick(self, event):
        if self.exitButton.underMouse():
            pass
        elif self.minimizeButton.underMouse():
            pass
        elif self.restoreButton.underMouse():
            pass
        else:
            self.prevPos = event.globalPosition().toPoint()

    def toolbarMove(self, event):
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
