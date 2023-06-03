import sys

from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy, QPlainTextEdit

from app.baseWindows import windowWithToolbar
from utils.databaseUtils import *


class employeeInfo(windowWithToolbar):
    def __init__(self, ID, parent=None):
        super().__init__(parent)
        self.exitButton.disconnect()  # removes any exit functions linked to button, so it doesn't close the entire program
        self.exitButton.clicked.connect(self.close)
        self.ID = ID

        self._medicalData = manageEmployee.getMedical(ID)
        self.initEmployeeData()
        self.initFooter()

    def initEmployeeData(self):
        empData = manageEmployee.get(self.ID)
        layout = QVBoxLayout()
        frame = QFrame()
        nameLabel = QLabel(f"{empData['firstName']} {empData['lastName']}")
        idLabel = QLabel(f"Employee ID: {self.ID}")
        designationLabel = QLabel(f"Designation: {empData['designation']}")
        startDateLabel = QLabel(f"Start Date: {empData['startDate']}")
        endDateLabel = QLabel(f"End Date: {empData['endDate']}")
        summaryLabel = QLabel("Summary:")
        summary = QPlainTextEdit(empData["summary"])
        summary.setReadOnly(True)
        summary.setFrameStyle(QFrame.Shape.NoFrame)
        summary.setAutoFillBackground(True)
        summary.setBackgroundRole(QPalette.ColorRole.NoRole)
        summary.setStyleSheet("background-color: transparent;")
        labels = [nameLabel, idLabel, designationLabel, startDateLabel,
                  endDateLabel, summaryLabel, summary]

        for label in labels:
            layout.addWidget(label)

        # pushes all the labels to the top of the layout
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        frame.setLayout(layout)
        self.primaryGridLayout.addWidget(frame, 1, 0)
        # TODO: implement a collapsible section for medical information


"""app = QApplication(sys.argv)
w = employeeInfo("E0442115")
w.show()
app.exec()"""
