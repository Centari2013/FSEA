import sys

from PyQt6 import QtWidgets
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy, QPlainTextEdit

from app.baseWindows import windowWithToolbar
#from app.customQWidgets import CollapsibleSection
from utils.databaseUtils import *


class infoWindowBase(windowWithToolbar):
    def __init__(self, ID, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollAreaContents = QtWidgets.QWidget()
        self.scrollAreaContentsFrame = QtWidgets.QFrame(self.scrollAreaContents)
        self.scrollAreaVLayout = QtWidgets.QVBoxLayout(self.scrollAreaContents)  # vertical layout for scrollAreaContentsFrame

        self.scrollArea.setWidget(self.scrollAreaContents)
        self.scrollAreaContents.setLayout(self.layout)


        self.exitButton.disconnect()  # removes any exit functions linked to button, so it doesn't close the entire program
        self.exitButton.clicked.connect(self.close) # connects the widget's close function to the exit button instead
        self.ID = ID

        self.initFooter()
        qargs = [QLabel("hi!") for i in range(10)]
        #self.colaap = CollapsibleSection('Collapsible', *qargs, parent=self)




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
        summary = QPlainTextEdit(empData["summary"])
        summary.setReadOnly(True)
        summary.setFrameStyle(QFrame.Shape.NoFrame)
        summary.setAutoFillBackground(True)
        summary.setBackgroundRole(QPalette.ColorRole.NoRole)
        summary.setStyleSheet("background-color: transparent;")
        labels = [nameLabel, idLabel, designationLabel, startDateLabel,
                  endDateLabel, summaryLabel, summary]




        for label in labels:
            self.layout.addWidget(label)

        #self.layout.addWidget(self.colaap)

        # pushes all the labels to the top of the layout
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)

        frame.setLayout(self.layout)
        self.primaryGridLayout.addWidget(frame, 1, 0)
        # TODO: implement a collapsible section for medical information


"""app = QApplication(sys.argv)
w = employeeInfo("E7449700")
w.show()
app.exec()
"""