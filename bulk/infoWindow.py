from PyQt6.QtWidgets import *
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtCore import QEvent
from utils.accessDatabaseUtils import *
from bulk.baseWindows import windowWithToolbar


class employeeInfo(windowWithToolbar):
    def __init__(self, empID):
        super().__init__()
        self.exitButton.clicked.connect(self.close)
        self.empID = empID

        self.empData = getEmployeeData(empID)
        self.medicalData = getEmployeeMedicalData(empID)

        layout = QGridLayout()
        self.setLayout(layout)
