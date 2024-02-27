from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from old_code.utils.filePaths import icons
from old_code.src.stylePresets import colors, stylesheets


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

    def __init__(self, text, func=None, args: tuple=None):
        super().__init__(text)
        self.setStyleSheet('border: 0px; padding: 0px;')
        self.function = func
        self.args = args

    def mouseReleaseEvent(self, event):
        if self.rect().contains(event.pos()):
            if self.function is not None:
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


class CollapsibleSection(QFrame):
    def __init__(self, title="", *content: QWidget, parent=None):
        super().__init__(parent)
        self._collapsedIcon = QIcon(icons["COLLAPSED_ARROW"])
        self._expandedIcon = QIcon(icons["EXPANDED_ARROW"])
        self.arrowButton = QPushButton()
        self.titleLabel = QLabel(title)
        self.titleFrame = QFrame(self)

        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.contentFrameH = QFrame(self)
        self.contentFrameHLayout = QHBoxLayout()
        self.contentFrameV = QFrame(self)
        self.contentFrameVLayout = QVBoxLayout(self)

        self.init_ui(*content)

    def init_ui(self, *content: QWidget):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.arrowButton.setCheckable(True)
        self.arrowButton.setFlat(True)
        self.arrowButton.setStyleSheet(stylesheets["COLLAPSIBLE_BUTTON"])
        self.arrowButton.toggled.connect(self._toggle_collapse)
        self.arrowButton.setFixedSize(16, 16)

        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.titleLabel.setStyleSheet("font-weight: bold;")

        titleFrameLayout = QHBoxLayout()
        titleFrameLayout.setContentsMargins(5, 0, 5, 0)
        titleFrameLayout.addWidget(self.arrowButton)
        titleFrameLayout.addWidget(self.titleLabel)

        self.titleFrame.setLayout(titleFrameLayout)
        self.contentFrameH.setLayout(self.contentFrameHLayout)
        self.contentFrameHLayout.setContentsMargins(0, 0, 0, 0)
        self.contentFrameV.setLayout(self.contentFrameVLayout)
        self.contentFrameVLayout.setContentsMargins(0, 0, 0, 0)

        # Set up visual indent for content in widget
        self.contentFrameHLayout.addSpacing(20)

        self.setContent(*content)

        layout.addWidget(self.titleFrame)
        layout.addWidget(self.contentFrameH)

        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setLayout(layout)

        self._toggle_collapse()

    def _toggle_collapse(self):
        if not self.arrowButton.isChecked():
            self.arrowButton.setIcon(self._collapsedIcon)
            self.contentFrameH.hide()
        else:
            self.arrowButton.setIcon(self._expandedIcon)
            self.contentFrameH.show()

    def setTitle(self, title: str):
        self.titleLabel.setText(title)

    def setContent(self, *content: QWidget):
        for i in reversed(range(self.contentFrameVLayout.count() )):
            self.contentFrameVLayout.itemAt(i).widget().setParent(None)

        for w in content:
            w.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            self.contentFrameVLayout.addWidget(w)
        self.contentFrameHLayout.addWidget(self.contentFrameV)


class headerLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(stylesheets["HEADER_LABEL"])

