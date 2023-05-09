def createEmployeeSpecimenTable(cur):
    cur.execute('''CREATE TABLE EmployeeSpecimen(
                    empID       TEXT NOT NULL,
                    specimenID  TEXT NOT NULL,
                   PRIMARY KEY (empID, specimenID),
                   CONSTRAINT employeeID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE, 
                   CONSTRAINT specimenID FOREIGN KEY (specimenID) REFERENCES Specimen(specimenID) ON DELETE CASCADE
                   );''')
    print('EmployeeSpecimen table created\n')


def dropEmployeeSpecimenTable(cur):
    # drop EmployeeSpecimen table from database if it exists
    try:
        cur.execute('''DROP TABLE EmployeeSpecimen''')

        print('EmployeeSpecimen table dropped\n')

    except:
        print('EmployeeSpecimen table does not exist\n')


def createEmployeeMissionTable(cur):
    cur.execute('''CREATE TABLE EmployeeMission(
                    empID  TEXT NOT NULL,
                    missionID TEXT NOT NULL,
                    involvementSummary TEXT DEFAULT NULL,
                    PRIMARY KEY (empID, missionID),
                    CONSTRAINT empID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE,
                    CONSTRAINT missionID FOREIGN KEY (missionID) REFERENCES Mission(missionID) ON DELETE CASCADE 
                    );''')
    print('EmployeeMission table created\n')


def dropEmployeeMissionTable(cur):
    # drop EmployeeMission table from database if it exists
    try:
        cur.execute('''DROP TABLE EmployeeMission''')

        print('EmployeeMission table dropped\n')

    except:
        print('EmployeeMission table does not exist\n')


def createSpecimenMission(cur):
    cur.execute('''CREATE TABLE SpecimenMission(
                    specimenID  TEXT NOT NULL,
                    missionID TEXT NOT NULL,
                    involvementSummary TEXT DEFAULT NULL,
                    PRIMARY KEY (specimenID, missionID),
                    CONSTRAINT specimenID FOREIGN KEY (specimenID) REFERENCES Specimen(specimenID) ON DELETE CASCADE,
                    CONSTRAINT missionID FOREIGN KEY (missionID) REFERENCES Mission(missionID) ON DELETE CASCADE 
                    );''')
    print('SpecimenMission table created\n')


def dropSpecimenMissionTable(cur):
    # drop SpecimenMission table from database if it exists
    try:
        cur.execute('''DROP TABLE SpecimenMission''')

        print('SpecimenMission table dropped\n')

    except:
        print('SpecimenMission table does not exist\n')


def createDepartmentMissionTable(cur):
    cur.execute('''CREATE TABLE DepartmentMission(
                    depID  TEXT NOT NULL,
                    missionID TEXT NOT NULL, 
                    PRIMARY KEY (depID, missionID),
                    CONSTRAINT depID FOREIGN KEY (depID) REFERENCES Department(depID) ON DELETE CASCADE,
                    CONSTRAINT missionID FOREIGN KEY (missionID) REFERENCES Mission(missionID) ON DELETE CASCADE 
                    );''')
    print('DepartmentMission table created\n')


def dropDepartmentMissionTable(cur):
    # drop DepartmentMission table from database if it exists
    try:
        cur.execute('''DROP TABLE DepartmentMission''')

        print('DepartmentMission table dropped\n')

    except:
        print('DepartmentMission table does not exist\n')


def createEmployeeDesignationTable(cur):
    # create EmployeeDesignation table in db
    cur.execute('''CREATE TABLE EmployeeDesignation(
                        empID TEXT NOT NULL,
                        designationID     INTEGER NOT NULL,
                        PRIMARY KEY (empID),
                        FOREIGN KEY (empID) REFERENCES Employee(empID),
                        FOREIGN KEY (designationID) REFERENCES Designation(designationID)
                        );''')

    print('Designation table created\n')


def dropEmployeeDesignationTable(cur):
    # drop EmployeeDesignation table from database if it exists
    try:
        cur.execute('''DROP TABLE EmployeeDesignation''')

        print('EmployeeDesignation table dropped\n')

    except:
        print('EmployeeDesignation table does not exist\n')
