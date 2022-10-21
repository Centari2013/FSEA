from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtGui, QtWidgets

# TODO fix drag and button overlay
class windowWithToolbar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.prevPos = None

        sizePolicy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setMinimumSize(QtCore.QSize(550, 345))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.setAutoFillBackground(False)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: #E3E4EA;")
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.titlebar = QtWidgets.QFrame(self.centralwidget)
        self.titlebar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.titlebar.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.titlebar.setStyleSheet("background-color: #31353D;\n"
                                    "color: white;")
        self.titlebar.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.titlebar.setObjectName("titlebar")
        self.gridLayout_2.addWidget(self.titlebar, 0, 0, 1, 2)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.titlebar)
        self.horizontalLayout.setContentsMargins(15, 5, -1, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.title = QtWidgets.QLabel("F-SEA Database")
        self.title.setObjectName("title")
        self.horizontalLayout.addWidget(self.title)

        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.spacerItem)


        self.minimizeButton = QtWidgets.QPushButton(self.titlebar)
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
        self.horizontalLayout.addWidget(self.minimizeButton)

        self.restoreButton = QtWidgets.QPushButton(self.titlebar)

        def minOrMax():
            if self.isMaximized():
                self.showNormal()
                # self.restoreButton.setStyleSheet("border-image: url(bulk/assets/restore.png);")
            elif not self.isMaximized():
                self.showMaximized()
                # self.restoreButton.setStyleSheet("border-image: url(bulk/assets/maximize.png);")

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
        self.horizontalLayout.addWidget(self.restoreButton)

        self.exitButton = QtWidgets.QPushButton(self.titlebar)
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)
        self.exitButton.setMinimumSize(QtCore.QSize(18, 18))
        self.exitButton.setMaximumSize(QtCore.QSize(18, 18))
        self.exitButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.exitButton.setStyleSheet("QPushButton { color: white;\n"
                                      "background-color: #31353D;\n"
                                      "border-image: url(bulk/assets/closeButton.png); }\n"
                                      "QPushButton::pressed { background-color: #111314; }")

        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)

        self.titlebar.mousePressEvent = lambda event: self.toolbarClick(event)
        self.titlebar.mouseMoveEvent = lambda event: self.toolbarMove(event)

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
                # TODO fix NoneType object return from clicked
                clicked = self.childAt(QPoint(event.globalPosition().toPoint()))
                self.move(clicked.mapFromGlobal(QPoint(event.globalPosition().toPoint())))

            delta = QPoint(event.globalPosition().toPoint() - self.prevPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.prevPos = event.globalPosition().toPoint()