from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QScrollBar, \
    QScrollArea
from app.stylePresets import colors



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




class CollapsibleSection(QFrame):
    def __init__(self, title, *content: QWidget, parent=None):
        super().__init__(parent)

        self.title = title

        self.arrowButton = QPushButton()
        self.titleLabel = QLabel(self.title)

        self.titleFrame = QFrame(self)

        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.contentFrame = QFrame()

        self.init_ui(*content)

    def init_ui(self, *content: QWidget):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.arrowButton.setCheckable(True)
        self.arrowButton.setFlat(True)
        self.arrowButton.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }

            QPushButton:checked {
                background-color: transparent;
            }

            QPushButton:hover {
                background-color: none;
            }
        """)
        self.arrowButton.toggled.connect(self._toggle_collapse)
        self.arrowButton.setFixedWidth(16)
        self.arrowButton.setFixedHeight(16)

        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.titleLabel.setStyleSheet("font-weight: bold;")

        titleFrameLayout = QHBoxLayout()
        titleFrameLayout.addWidget(self.arrowButton)
        titleFrameLayout.addWidget(self.titleLabel)

        self.titleFrame.setLayout(titleFrameLayout)

        contentFrameLayout = QVBoxLayout()
        self.contentFrame.setLayout(contentFrameLayout)

        for w in content:
            w.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            contentFrameLayout.addWidget(w)


        layout.addWidget(self.titleFrame)
        layout.addWidget(self.contentFrame)

        #self.contentFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setLayout(layout)

        self._toggle_collapse()

    def _toggle_collapse(self):
        if not self.arrowButton.isChecked():
            arrow = "▶"
            self.contentFrame.hide()
        else:
            arrow = "▼"
            self.contentFrame.show()
        self.arrowButton.setText(arrow)





