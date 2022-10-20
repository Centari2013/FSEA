from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class draggableFrameless(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.prevPos = None

    def mousePressEvent(self, event):
        self.prevPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.prevPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.prevPos = event.globalPosition().toPoint()
