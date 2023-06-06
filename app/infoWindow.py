import sys

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication, QGridLayout, QScrollArea, QWidget
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy, QPlainTextEdit

from app.baseWindows import windowWithToolbar
from app.customQWidgets import CollapsibleSection, ElidedLabel, IdLabel
from utils.databaseUtils import *
from utils.dbVariables import employeeType





class infoWindowBase(windowWithToolbar):
    def __init__(self, ID, parent=None):
        super().__init__(parent)
        self.scrollArea = QScrollArea()
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.layout)
        self.scrollArea.setWidget(self.scrollWidget)

        self.exitButton.disconnect()  # removes any exit functions linked to button, so it doesn't close the entire program
        self.exitButton.clicked.connect(self.close) # connects the widget's close function to the exit button instead
        self.ID = ID

        qargs = [QLabel("hi!") for _ in range(10)]
        self.collapsibleSection = CollapsibleSection('Collapsible', *qargs, parent=self)

        self.primaryGridLayout.addWidget(self.scrollArea, 1, 0)
        self.initFooter()


class employeeInfo(infoWindowBase):
    def __init__(self, ID, parent=None):
        super().__init__(ID, parent)
        self._medicalData = manageEmployee.getMedical(ID)
        dID = manageEmployeeDesignation.get(self.ID)['designationID']
        self._designationData = manageDesignation.get(dID)

        self.initEmployeeData()
        self.initFooter()

    def initEmployeeData(self):
        empData = manageEmployee.get(self.ID)

        frame = QFrame()
        nameLabel = QLabel(f"{empData['firstName']} {empData['lastName']}")
        idLabel = QLabel(f"Employee ID: {self.ID}")

        designationLabel = QLabel(f"Designation: {self._designationData['name']}")
        startDateLabel = QLabel(f"Start Date: {empData['startDate']}")
        endDateLabel = QLabel(f"End Date: {empData['endDate']}")
        summaryLabel = QLabel("Summary:")
        summary = QLabel(empData["summary"])
        summary.setWordWrap(True)
        labels = [nameLabel, idLabel, designationLabel, startDateLabel, endDateLabel, summaryLabel, summary]

        for label in labels:
            self.layout.addWidget(label)

        self.layout.addSpacerItem(QSpacerItem(1, 20))
        self.layout.addWidget(self.collapsibleSection)

        frame.setLayout(self.layout)
        self.primaryGridLayout.addWidget(frame, 1, 0)

        # TODO: implement a collapsible section for medical information


app = QApplication(sys.argv)
w = employeeInfo("E0136531")
w.show()
app.exec()
