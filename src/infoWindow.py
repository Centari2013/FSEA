import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QScrollArea, QWidget, QLabel, QFrame, QTableWidget, \
    QTableWidgetItem
from src.baseWindows import windowWithTitleBar
from src.customQWidgets import CollapsibleSection, headerLabel, IdLabel
from utils.databaseUtils import *
from src.stylePresets import stylesheets


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

class MissionInfo(InfoWindowBase):
    def __init__(self, missionID, parent=None):
        super().__init__(missionID, parent)
        self._missionData = None
        self._employeeInvolvement = None
        self._departmentInvolvement = None

        self._initMissionData()

    def _initMissionData(self):
        self._missionData = manageMission.get(self.ID)
        self._employeeInvolvement = manageMission.getEmployeeByMissionID(self.ID)
        self._departmentInvolvement = manageMission.getDepartmentByMissionID(self.ID)

    def _initDataGUI(self):
        nameLabel = headerLabel(f"{self._missionData['name']}")
        idLabel = QLabel(f"Mission ID: {self.ID}")
        originIdText = IdLabel("Origin ID: ")
        startDateLabel = QLabel(f"Start Date: {self._empData['startDate']}")
        endDateLabel = QLabel(f"End Date: {self._empData['endDate']}")
        summaryLabel = QLabel("Summary:")
        summary = QLabel(self._empData["summary"])
        summary.setWordWrap(True)
        labels = [nameLabel, idLabel, originIdText, startDateLabel, endDateLabel, summaryLabel, summary]

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

        medicalLayout.addWidget(DataTable(medData))

        medicalFrame.setLayout(medicalLayout)

        self._medicalSection.setTitle("Medical Data")
        self._medicalSection.setContent(medicalFrame)

        self.layout.addWidget(self._medicalSection)

        self._missionSection.setTitle("Mission Involvement")
        if self._involvedMissions is not None:
            missionList = [m["missionID"] for m in self._involvedMissions]
            self._missionSection.setContent(MissionInvolvementView(missionList))

        self.layout.addWidget(self._missionSection)

class EmployeeInfo(InfoWindowBase):
    def __init__(self, empID, parent=None):
        super().__init__(empID, parent)
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


    def _initDataGUI(self):
        nameLabel = headerLabel(f"{self._empData['firstName']} {self._empData['lastName']}")
        summary = QLabel()
        summary.setWordWrap(True)

        empData = {"Employee ID:": [self.ID],
                   "Designation:": [self._designationData["name"]],
                   "Start Date:": [self._empData["startDate"]],
                   "End Date:": [self._empData["endDate"]],
                   "Summary:": []}

        self.layout.addWidget(nameLabel)
        self.layout.addWidget(DataTable(empData))
        self.layout.addWidget(summary)


        # medical data setup
        medicalFrame = QFrame(self._medicalSection)
        medicalLayout = QVBoxLayout(medicalFrame)

        medData = {"DOB:": [self._medicalData["dob"]],
                   "Blood Type:": [self._medicalData["bloodtype"]],
                   "Sex:": [self._medicalData["sex"]],
                   "Weight (kg):": [str(self._medicalData["kilograms"])],
                   "Height (cm):": [str(self._medicalData["height"])],
                   "Notes:": [self._medicalData["notes"]]}


        medicalLayout.addWidget(DataTable(medData))

        medicalFrame.setLayout(medicalLayout)
        self.layout.addSpacing(100)
        self._medicalSection.setTitle("Medical Data")
        self._medicalSection.setContent(medicalFrame)

        self.layout.addWidget(self._medicalSection)

        self._missionSection.setTitle("Mission Involvement")
        if self._involvedMissions is not None:
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


class DataTable(QTableWidget):
    def __init__(self, data):
        super(DataTable, self).__init__()
        self.data = data
        self.setStyleSheet("background-color: blue;")
        self.setData()
        self.setContentsMargins(0,0,0,0)
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
                try:
                    new_item = QTableWidgetItem(item)
                    self.setItem(n, 0, new_item)  # Set item in the same row (n) but in the first column (0)
                except:
                    self.setCellWidget(n, 0, item)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()



app = QApplication(sys.argv)
w = EmployeeInfo("E2676502")
w.show()
app.exec()
