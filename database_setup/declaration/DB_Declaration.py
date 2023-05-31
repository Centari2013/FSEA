import sqlite3
from utils.filePaths import DB_PATH
from database_setup.declaration.securityTables import *
from database_setup.declaration.departmentTables import *
from database_setup.declaration.employeeTables import *
from database_setup.declaration.originTables import *
from database_setup.declaration.missionTables import *
from database_setup.declaration.specimenTables import *
from database_setup.declaration.bridgeTables import *
from database_setup.declaration.searchResultsTables import *

# create new db (or open if already exists)
con = sqlite3.connect(DB_PATH)

# create cursor for statement execution
cur = con.cursor()

# drop fts tables
dropDepartment_ftsTable(cur)
dropEmployee_ftsTable(cur)
dropSpecimen_ftsTable(cur)
dropOrigin_ftsTable(cur)
dropMission_ftsTable(cur)
dropSearchResultsTable(cur)
con.commit()

# drop all security-related tables
dropClearanceTable(cur)
dropContainmentStatusTable(cur)
dropEmployeeClearanceTable(cur)
dropSpecimenContainmentStatusTable(cur)
dropCredentialsTable(cur)

# drop all other linked tables
dropDepartmentMissionTable(cur)
dropResearcherSpecimenTable(cur)
dropEmployeeMissionTable(cur)
dropSpecimenMissionTable(cur)
dropSpecimenMedicalTable(cur)
dropOriginTable(cur)
dropMissionTable(cur)
dropSpecimenTable(cur)
dropEmployeeMedicalTable(cur)
dropEmployeeDesignationTable(cur)
dropDesignationTable(cur)
dropEmployeeTable(cur)
dropDepartmentTable(cur)
con.commit()


# create all tables
createDepartmentTable(cur)
con.commit()

createDesignationTable(cur)
createEmployeeTable(cur)
createEmployeeDesignationTable(cur)
createEmployeeMedicalTable(cur)
con.commit()

createCredentialsTable(cur)
createClearanceTable(cur)
createContainmentStatusTable(cur)
createEmployeeClearanceTable(cur)
createSpecimenContainmentStatusTable(cur)
con.commit()

createOriginTable(cur)
con.commit()

createMissionTable(cur)
con.commit()

createSpecimenTable(cur)
createSpecimenMedicalTable(cur)
con.commit()


# create bridge tables
createResearcherSpecimenTable(cur)
createEmployeeMissionTable(cur)
createSpecimenMission(cur)
createDepartmentMissionTable(cur)
con.commit()

# create FTS tables
createEmployee_ftsTable(cur)
createSpecimen_ftsTable(cur)
createDepartment_ftsTable(cur)
createOrigin_ftsTable(cur)
createMission_ftsTable(cur)
con.commit()


# create table triggers
createEmployeeTriggers(cur)
createSpecimenTriggers(cur)
createDepartmentTriggers(cur)
createOriginTriggers(cur)
createMissionTriggers(cur)
con.commit()

# create search results table
createSearchResultsTable(cur)
con.commit()


con.close()
