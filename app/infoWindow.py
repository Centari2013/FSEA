import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QScrollArea, QWidget, QLabel, QFrame, QTableWidget, \
    QTableWidgetItem
from app.baseWindows import windowWithTitleBar
from app.customQWidgets import CollapsibleSection, headerLabel, IdLabel
from utils.databaseUtils import *
from app.stylePresets import stylesheets


class InfoWindowBase(windowWithTitleBar):
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


class EmployeeInfo(InfoWindowBase):
    def __init__(self, ID, parent=None):
        super().__init__(ID, parent)
        self.ID = ID
        self._empData = None
        self._medicalData = None
        self._medicalSection = CollapsibleSection()

        self._designationData = None

        self._involvedMissions = None
        self._missionSection = CollapsibleSection()
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
        print(self._involvedMissions)

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

        medData = {"DOB:": [self._medicalData["dob"]],
                   "Blood Type:": [self._medicalData["bloodtype"]],
                   "Sex:": [self._medicalData["sex"]],
                   "Weight (kg):": [str(self._medicalData["kilograms"])],
                   "Height (cm):": [str(self._medicalData["height"])],
                   "Notes:": [self._medicalData["notes"]]}


        medicalLayout.addWidget(MedicalTable(medData))

        medicalFrame.setLayout(medicalLayout)

        self._medicalSection.setTitle("Medical Data")
        self._medicalSection.setContent(medicalFrame)

        self.layout.addWidget(self._medicalSection)

        self._missionSection.setTitle("Mission Involvement")
        missionList = [m["missionID"] for m in self._involvedMissions]
        self._missionSection.setContent(MissionInvolvementView(missionList))

        self.layout.addWidget(self._missionSection)



class MissionInvolvementView(QFrame):
    def __init__(self, missionList: list[str]):
        super(MissionInvolvementView, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for m in missionList:
            self.layout.addWidget(IdLabel(m))


class MedicalTable(QTableWidget):
    def __init__(self, data):
        super(MedicalTable, self).__init__()
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setShowGrid(False)
        font = QFont()
        font.setBold(True)
        self.verticalHeader().setFont(font)

        self.setStyleSheet(
            "QTableWidget { background-color: transparent; border: none; }"
            "QHeaderView::section { background-color: transparent; border: none; color: dimgray;}"
            "QTableWidget::item { border: none; }"
        )
        self.horizontalHeader().setVisible(False)

    def setData(self):
        keys = sorted(self.data.keys())
        self.setColumnCount(1)  # Set column count to 1 since we only need one column for the values
        self.setRowCount(len(keys))  # Set row count to the number of keys

        for n, key in enumerate(keys):
            self.setVerticalHeaderItem(n, QTableWidgetItem(key))  # Set key as vertical header item
            items = self.data[key]
            for m, item in enumerate(items):
                new_item = QTableWidgetItem(item)
                self.setItem(n, 0, new_item)  # Set item in the same row (n) but in the first column (0)


        self.resizeColumnsToContents()
        self.resizeRowsToContents()



app = QApplication(sys.argv)
w = EmployeeInfo("E2676502")
w.show()
app.exec()
