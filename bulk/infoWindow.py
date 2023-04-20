from utils.accessDatabaseUtils import *
from bulk.baseWindows import windowWithToolbar


class employeeInfo(windowWithToolbar):
    def __init__(self, empID, parent=None):
        super().__init__(parent)
        self.exitButton.disconnect() # removes any exit functions linked to button so it doesn't close the entire program
        self.exitButton.clicked.connect(self.close)
        self.empID = empID

        self._empData = getEmployeeData(empID)
        self._medicalData = getEmployeeMedicalData(empID)

