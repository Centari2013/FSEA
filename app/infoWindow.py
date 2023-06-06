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


class infoWindowBase(windowWithToolbar):
    def __init__(self, ID, parent=None):
        super().__init__(parent)
        self.scrollArea = QScrollArea()
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.scrollArea.setWidgetResizable(True)

        self.layout = QVBoxLayout()
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.layout)
        self.scrollArea.setWidget(self.scrollWidget)


        self.exitButton.disconnect()  # removes any exit functions linked to button, so it doesn't close the entire program
        self.exitButton.clicked.connect(self.close) # connects the widget's close function to the exit button instead
        self.ID = ID

        self.initFooter()
        qargs = [QLabel("hi!") for i in range(10)]
        self.colaap = CollapsibleSection('Collapsible', *qargs, parent=self)
        self.layout.addWidget(self.colaap)

        self.primaryGridLayout.addWidget(self.scrollArea, 1, 0)



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

        self.layout.addWidget(self.colaap)


        # pushes all the labels to the top of the layout
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)

        frame.setLayout(self.layout)
        self.primaryGridLayout.addWidget(frame, 1, 0)
        # TODO: implement a collapsible section for medical information


app = QApplication(sys.argv)
w = employeeInfo("E7449700")
w.show()
app.exec()
