import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
from app.colorPresets import colors
from utils.filePaths import icons


class windowWithToolbar(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint) # allows for custom title bar
        self.setWindowModality(Qt.WindowModality.NonModal) # window does not take priority above all else
        self.prevPos = None # used to define draggable window behavior

        self.setMinimumSize(QtCore.QSize(550, 430))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

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

    def add_titlebar_button(self, button, name, iconPath, click_function):
        button.setObjectName(name)
        button.clicked.connect(click_function)
        button.setMinimumSize(QtCore.QSize(18, 18))
        button.setMaximumSize(QtCore.QSize(18, 18))
        button.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        button.setIcon(QIcon(iconPath))
        button.setStyleSheet("QPushButton { color: white;\n"
                             "background-color: %s;\n"
                             "border: none; }\n"
                             "QPushButton::pressed { background-color: %s; }" % (
                                 colors["TITLEBAR_BUTTON_COLOR"],
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

        # separates buttons from title QLabel
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.titlebarLayout.addItem(spacerItem)

        self.add_titlebar_button(self.minimizeButton, "minimize", icons['MINIMIZE_BUTTON'], self.showMinimized)
        self.add_titlebar_button(self.restoreButton, "restore", icons['RESTORE_BUTTON'], self._minOrMax)
        self.add_titlebar_button(self.exitButton, "exit", icons['EXIT_BUTTON'], sys.exit)

        self.primaryGridLayout.addWidget(self.titlebarFrame, 0, 0, 1, 2)

    def initFooter(self, *widgetList: QWidget):
        """
        Must be called to make window resizable.

        *widgetList: list of QWidgets to add to footer
        returns None
        """
        self.footerFrame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.footerFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.footerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.footerFrame.setObjectName("footerFrame")

        self.footerLayout.setContentsMargins(0, 0, 0, 0)
        self.footerLayout.setObjectName("footerLayout")

        # automatically insert widgets into separate columns
        col = 0
        for w in widgetList:
            self.footerLayout.addWidget(w, 0, col, Qt.AlignmentFlag.AlignCenter)
            col += 1

        # make window resizable by inserting QSizeGrip to bottom right
        self.footerLayout.addWidget(QSizeGrip(self), 0, col, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.primaryGridLayout.addWidget(self.footerFrame, 3, 1)

    def _minOrMax(self):
        """
        defines restore and minimize button functionality
        :return: None
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def _toolbarClick(self, event: QWidget.mousePressEvent):
        """"
        sets self.pos to coordinates of click event
        """

        # ignore buttons when moving toolbar
        if self.exitButton.underMouse():
            pass
        elif self.minimizeButton.underMouse():
            pass
        elif self.restoreButton.underMouse():
            pass
        else:
            # set prevPos to where the click occurred
            self.prevPos = event.globalPosition().toPoint()

    def _toolbarMove(self, event: QWidget.mouseMoveEvent):
        """
    Move the toolbar based on the mouse movement.

    Parameters:
    - event (QMouseEvent): The mouse move event that triggered the toolbar movement.

    Description:
    - This method is called when the toolbar is being dragged by the user.
    - It calculates the movement delta based on the difference between the current mouse position and the previous position.
    - If the mouse is not over any of the toolbar buttons (exitButton, minimizeButton, restoreButton), the toolbar is moved accordingly.
    - If the window is maximized, it restores the window to its normal size and moves it by a fraction of its width and height to give a smooth movement effect.
    - Finally, it updates the previous position with the current mouse position for the next movement calculation.
    """
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
