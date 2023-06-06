import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QScrollArea, QWidget, QLabel, QFrame, QSpacerItem
from app.baseWindows import windowWithToolbar
from app.customQWidgets import CollapsibleSection
from utils.databaseUtils import *
from app.stylePresets import stylesheets


class infoWindowBase(windowWithToolbar):
    def __init__(self, ID, parent=None):
        super().__init__(parent)
        self.scrollArea = QScrollArea()
        bar = self.scrollArea.verticalScrollBar()
        bar.setStyleSheet(stylesheets["SCROLL_BAR"])
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.layout)
        self.scrollArea.setWidget(self.scrollWidget)

        self.exitButton.disconnect()
        self.exitButton.clicked.connect(self.close)
        self.ID = ID

        qargs = [QLabel("hi!") for _ in range(10)]
        self.collapsibleSection = CollapsibleSection('Collapsible', *qargs, parent=self)

        comfyLayout = QVBoxLayout()
        comfyLayout.setContentsMargins(0, 10, 0, 10)
        comfyLayout.addWidget(self.scrollArea)
        comfyFrame = QFrame()
        comfyFrame.setLayout(comfyLayout)

        self.primaryGridLayout.addWidget(comfyFrame, 1, 0)
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


app = QApplication(sys.argv)
w = employeeInfo("E0136531")
w.show()
app.exec()
