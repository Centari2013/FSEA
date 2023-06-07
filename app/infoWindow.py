import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QScrollArea, QWidget, QLabel, QFrame, QSpacerItem
from app.baseWindows import windowWithToolbar
from app.customQWidgets import collapsibleSection, headerLabel
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

        comfyLayout = QVBoxLayout()  # used to add content margins around scrollArea for better aesthetics
        comfyLayout.setContentsMargins(0, 10, 0, 10)
        comfyLayout.addWidget(self.scrollArea)
        comfyFrame = QFrame()
        comfyFrame.setLayout(comfyLayout)

        self.primaryGridLayout.addWidget(comfyFrame, 1, 0)
        self.initFooter()


class employeeInfo(infoWindowBase):
    def __init__(self, ID, parent=None):
        super().__init__(ID, parent)
        self.ID = ID
        self._empData = None
        self._medicalData = None
        self._medicalSection = collapsibleSection()

        self._designationData = None

        self._involvedMissions = None
        self._missionSection = collapsibleSection()
        self._clearance = None

        self._initEmployeeData()
        self._initDataGUI()
        self.initFooter()

    def _initEmployeeData(self):
        self._empData = manageEmployee.get(self.ID)
        self._medicalData = manageEmployee.getMedical(self.ID)

        dID = manageEmployeeDesignation.get(self.ID)['designationID']
        self._designationData = manageDesignation.get(dID)

        self._involvedMissions = manageMission.getMissionByEmpID(self.ID)

        cID = manageEmployee.getEmployeeClearance(self.ID)
        self._clearance = manageClearance.get(cID["clearanceID"])

    def _initDataGUI(self):
        nameLabel = headerLabel(f"{self._empData['firstName']} {self._empData['lastName']}")
        idLabel = QLabel(f"Employee ID: {self.ID}")
        designationLabel = QLabel(f"Designation: {self._designationData['name']}")
        startDateLabel = QLabel(f"Start Date: {self._empData['startDate']}")
        endDateLabel = QLabel(f"End Date: {self._empData['endDate']}")
        summaryLabel = QLabel("Summary:")
        summary = QLabel(self._empData["summary"])
        summary.setWordWrap(True)
        labels = [nameLabel, idLabel, designationLabel, startDateLabel, endDateLabel, summaryLabel, summary]

        for label in labels:
            self.layout.addWidget(label)

        # medical data setup
        medicalFrame = QFrame(self._medicalSection)
        medicalLayout = QVBoxLayout(medicalFrame)

        dob = QLabel("DOB: " + self._medicalData["dob"])
        bloodtype = QLabel("Blood Type: " + self._medicalData["bloodtype"])
        sex = QLabel("Sex: " + self._medicalData["sex"])
        kg = QLabel("Weight (kg): " + str(self._medicalData["kilograms"]))
        height = QLabel("Height (cm): " + str(self._medicalData["height"]))
        notes = QLabel("Notes: " + self._medicalData["notes"])
        notes.setWordWrap(True)

        labels = [dob, bloodtype, sex, kg, height, notes]

        for label in labels:
            medicalLayout.addWidget(label)

        medicalFrame.setLayout(medicalLayout)

        self._medicalSection.setTitle("Medical Data")
        self._medicalSection.setContent(medicalFrame)

        self.layout.addWidget(self._medicalSection)
        self.layout.addSpacerItem(QSpacerItem(1, 20))

    # TODO: Finish Employee page GUI


app = QApplication(sys.argv)
w = employeeInfo("E0136531")
w.show()
app.exec()
