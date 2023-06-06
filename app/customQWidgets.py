from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QGridLayout, QFrame, QPushButton
from app.colorPresets import colors
from app.infoWindow import employeeInfo
from utils.dbVariables import employeeType


class PanelButton(QPushButton):
    """
        A button class inherited from QPushButton.

        Added Attributes:
            flag (str): The type of panel button set by developer.

        Methods:
            QPushButton methods.
    """

    def __init__(self, buttonText, flag):
        super().__init__(buttonText)

        self.flag = flag
        self.setCheckable(True)
        self.clicked.connect(self._changeButtonColor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(100, 65))
        self.setStyleSheet("QPushButton { color: white;\n"
                           "background-color: %s;\n"
                           "border: none; }\n"
                           "QPushButton::pressed { background-color: %s; }" % (
                               colors["PUSH_BUTTON_COLOR"], colors["PUSH_BUTTON_PRESSED_COLOR"]))

    def _changeButtonColor(self):
        if self.isChecked():
            self.setStyleSheet("QPushButton { color: %s;\n"
                               "background-color: %s;\n"
                               "border: none; }\n"
                               "QPushButton::pressed { background-color: %s; }" % (
                                   colors["PUSH_BUTTON_TEXT_COLOR"], colors["PUSH_BUTTON_PRESSED_COLOR"],
                                   colors["PUSH_BUTTON_PRESSED_COLOR"]))
        else:
            self.setStyleSheet("QPushButton { color: %s;\n"
                               "background-color: %s;\n"
                               "border: none; }\n"
                               "QPushButton::pressed { background-color: %s; }" % (
                                   colors["PUSH_BUTTON_TEXT_COLOR"], colors["PUSH_BUTTON_COLOR"],
                                   colors["PUSH_BUTTON_PRESSED_COLOR"]))


class ElidedLabel(QLabel):
    """
            A label class inherited from QLabel that allows for long text to appear elided
            and when the label is expanded, more elided text is shown.

            Added Attributes:
                n/a

            Added Methods:
                n/a
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('border: 0px; padding: 0px;')

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        metrics = QtGui.QFontMetrics(self.font())
        elided = metrics.elidedText(self.text(), Qt.TextElideMode.ElideRight, self.width())
        painter.drawText(self.rect(), self.alignment(), elided)


class IdLabel(QLabel):
    """
            A label class inherited from QLabel that emulates a hyperlink when hovered over.

            Added Attributes:
                function (function): The function to be run after clicking the label.
                args (tuple): The arguments to pass to function

            Added Methods:
                n/a
    """

    def __init__(self, parent, func, args: tuple = None):
        super().__init__(parent)
        self.setStyleSheet('border: 0px; padding: 0px;')
        self.function = func
        self.args = args

    def mouseReleaseEvent(self, event):
        if self.rect().contains(event.pos()):
            if self.args is not None:
                self.function(*self.args)
            else:
                self.function()
        else:
            pass

    def enterEvent(self, event):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtGui.QColor('blue'))
        palette.setColor(self.foregroundRole(), QtGui.QColor('blue'))
        self.setPalette(palette)

        f = QtGui.QFont()
        f.setUnderline(True)
        self.setFont(f)

    def leaveEvent(self, event):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtGui.QColor('black'))
        palette.setColor(self.foregroundRole(), QtGui.QColor('black'))
        self.setPalette(palette)

        f = QtGui.QFont()
        f.setUnderline(False)
        self.setFont(f)


class SearchResult(QFrame):
    """
            A frame inherited from QFrame that is used to populate
            search results

            Added Attributes:
                idLabel (IdLabel): The clickable QLabel
                id (str): The ID you want to show in the idLabel.

            Added Methods:
                openInfoWindow(): opens window with more info on the search results

            *Note: If firstName is None, then only the lastName will show on the frame.
    """

    def __init__(self, parent=None, ID: str = None, resultType=None, lastName=None, firstName=None, description=None):
        super(SearchResult, self).__init__(parent=None)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(0, 90))
        self.setMaximumSize(QtCore.QSize(16777215, 100))
        self.setAutoFillBackground(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setObjectName("search_label")
        self.setStyleSheet("border: 1px solid gray; padding: 6;")

        self._gridLayout = QGridLayout(parent)

        self.id = ID
        self._lastName = lastName
        self._firstName = firstName
        self._description = description
        self._type = resultType

        # allows for entities with only one name to use this class
        if firstName is not None:
            nameLabel = ElidedLabel(f'{self._lastName},  {self._firstName}')
        else:
            nameLabel = ElidedLabel(self._lastName)

        self.idLabel = IdLabel(self.id, self.openInfoWindow)

        self._gridLayout.addWidget(self.idLabel, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self._gridLayout.addWidget(nameLabel, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self._gridLayout.addWidget(ElidedLabel(self._description), 2, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self._gridLayout.setColumnStretch(0, 1)
        self._gridLayout.setColumnStretch(1, 20)
        self._gridLayout.setColumnStretch(2, 0)

        self.setLayout(self._gridLayout)
        self._window = None

    def openInfoWindow(self):
        if self._type == employeeType:
            self._window = employeeInfo(self.id)
            self._window.show()