def createClearanceTable(cur):
    # create Clearance table
    cur.execute('''CREATE TABLE Clearance(
                        clearanceID      INTEGER UNIQUE NOT NULL,
                        name TEXT,
                        description TEXT,
                        PRIMARY KEY (clearanceID)
                        );''')
    print('Clearance table created\n')


def dropClearanceTable(cur):
    # drop Clearance table from database if it exists
    try:
        cur.execute('''DROP TABLE Clearance''')

        print('Clearance table dropped\n')

    except:
        print('Clearance table does not exist\n')


def createContainmentStatusTable(cur):
    # create ContainmentStatus table
    cur.execute('''CREATE TABLE ContainmentStatus(
                        containmentStatusID      INTEGER UNIQUE NOT NULL,
                        name TEXT,
                        description TEXT,
                        PRIMARY KEY (containmentStatusID)
                        );''')
    print('ContainmentStatus table created\n')


def dropContainmentStatusTable(cur):
    # drop ContainmentStatus table from database if it exists
    try:
        cur.execute('''DROP TABLE ContainmentStatus''')

        print('ContainmentStatus table dropped\n')

    except:
        print('ContainmentStatus table does not exist\n')


def createEmployeeClearanceTable(cur):
    # create EmployeeClearance table
    cur.execute('''CREATE TABLE EmployeeClearance(
                    empID           TEXT NOT NULL UNIQUE,
                    clearanceID      INTEGER,
                    PRIMARY KEY (empID),
                    CONSTRAINT employeeID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE,
                    CONSTRAINT clearanceID FOREIGN KEY (clearanceID) REFERENCES Clearance(clearanceID) ON DELETE CASCADE
                    );''')
    print('EmployeeClearance table created\n')


def dropEmployeeClearanceTable(cur):
    # drop EmployeeClearance table from database if it exists
    try:
        cur.execute('''DROP TABLE EmployeeClearance''')

        print('EmployeeClearance table dropped\n')

    except:
        print('EmployeeClearance table does not exist\n')


def createSpecimenContainmentStatusTable(cur):
    # create SpecimenContainmentStatus table
    cur.execute('''CREATE TABLE SpecimenContainmentStatus(
                    specimenID           TEXT NOT NULL UNIQUE,
                    containmentStatusID     INTEGER,
                    PRIMARY KEY (specimenID),
                    CONSTRAINT SpecimenID FOREIGN KEY (specimenID) REFERENCES Specimen(specimenID) ON DELETE CASCADE,
                    CONSTRAINT statusID FOREIGN KEY (containmentStatusID) REFERENCES ContainmentStatus(containmentStatusID) ON DELETE CASCADE
                    );''')
    print('SpecimenContainmentStatus table created\n')


def dropSpecimenContainmentStatusTable(cur):
    # drop SpecimeContainmentStatus table from database if it exists
    try:
        cur.execute('''DROP TABLE SpecimenContainmentStatus''')

        print('SpecimenContainmentStatus table dropped\n')

    except:
        print('SpecimenContainmentStatus table does not exist\n')


def createCredentialsTable(cur):
    # create Credentials table
    cur.execute('''CREATE TABLE Credentials(
                    empID           TEXT NOT NULL UNIQUE,
                    username        TEXT DEFAULT NULL,
                    password        TEXT DEFAULT NULL,
                    loginAttempts   INTEGER DEFAULT 0,
                    PRIMARY KEY (empID),
                    CONSTRAINT employeeID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE
                    );''')
    print('Credentials table created\n')


def dropCredentialsTable(cur):
    # drop Credentials table from database if it exists
    try:
        cur.execute('DROP TABLE Credentials')

        print('Credentials table dropped\n')

    except:
        print('Credentials table does not exist\n')
