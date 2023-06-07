from utils.dbVariables import designation, bloodtypes, sex

def createDesignationTable(cur):
    # create Designation table in db
    cur.execute('''CREATE TABLE Designation(
                        designationID     INTEGER NOT NULL UNIQUE,
                        name TEXT NOT NULL,
                        abbreviation TEXT NOT NULL,
                        PRIMARY KEY (designationID)
                        );''')

    print('Designation table created\n')

def dropDesignationTable(cur):
    # drop Designation table from database if it exists
    try:
        cur.execute('''DROP TABLE Designation''')

        print('Designation table dropped\n')

    except:
        print('Designation table does not exist\n')


def createEmployeeTable(cur):
    # create Employee table in db
    cur.execute('''CREATE TABLE Employee(
                    empDep          INTEGER NOT NULL,
                    empID           TEXT NOT NULL UNIQUE,
                    firstName       TEXT CHECK(LENGTH(firstName) <= 50) NOT NULL,
                    lastName        TEXT CHECK(LENGTH(lastName) <= 50)  NOT NULL,
                    startDate       TEXT NOT NULL,
                    endDate         TEXT DEFAULT NULL,
                    summary         TEXT DEFAULT '',
                    PRIMARY KEY (empID),
                    FOREIGN KEY (empDep) REFERENCES Department(depId)
                    );''')

    print('Employee table created\n')


def dropEmployeeTable(cur):
    # drop Employee table from database if it exists
    try:
        cur.execute('''DROP TABLE Employee''')

        print('Employee table dropped\n')

    except:
        print('Employee table does not exist\n')


def createEmployeeMedicalTable(cur):
    # create EmployeeMedical table in db
    cur.execute('''CREATE TABLE EmployeeMedical( 
                    empID           TEXT NOT NULL UNIQUE,
                    dob             TEXT DEFAULT NULL,
                    bloodtype       TEXT CHECK(bloodtype IN {}),
                    sex             TEXT CHECK(sex IN {}),
                    kilograms       REAL DEFAULT NULL,
                    height          REAL DEFAULT NULL,
                    notes           TEXT DEFAULT '',
                    PRIMARY KEY (empID),
                    CONSTRAINT  empID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE
                    );'''.format(bloodtypes, sex))

    print('EmployeeMedical table created\n')


def dropEmployeeMedicalTable(cur):
    # drop EmployeeMedical table from database if it exists
    try:
        cur.execute('''DROP TABLE EmployeeMedical''')

        print('EmployeeMedical table dropped\n')

    except:
        print('EmployeeMedical table does not exist\n')


def createEmployee_ftsTable(cur):
    cur.execute('''CREATE VIRTUAL TABLE Employee_fts USING fts5(
                    empID, 
                    empDep, 
                    designation, 
                    firstName, 
                    lastName, 
                    startDate UNINDEXED, 
                    endDate UNINDEXED,
                    summary,
                    tokenize="porter"  
                )''')
    print('Employee_fts table created\n')


def dropEmployee_ftsTable(cur):
    # drop Employee_fts table from database if it exists
    try:
        cur.execute('''DROP TABLE Employee_fts''')

        print('Employee_fts table dropped\n')

    except:
        print('Employee_fts table does not exist\n')


def createEmployeeTriggers(cur):
    cur.execute('''CREATE TRIGGER emp_inserts AFTER INSERT ON Employee
                    BEGIN
                        INSERT INTO Employee_fts (empID, empDep, firstName, lastName, summary)
                        VALUES (new.empID, new.empDep, new.firstName, new.lastName, new.summary);
                        UPDATE Employee_fts 
                        SET designation = (SELECT name FROM Designation 
                                            WHERE designationID IN (SELECT designationID 
                                                                    FROM EmployeeDesignation
                                                                    WHERE EmployeeDesignation.empID = new.empID));
                        INSERT INTO EmployeeMedical(empID)
                        VALUES (new.empID); 
                        INSERT INTO Credentials (empID)
                        VALUES (new.empID);
                        INSERT INTO EmployeeClearance (empID) 
                        VALUES (new.empID);
                    END;''')

    cur.execute('''CREATE TRIGGER emp_deletes AFTER DELETE ON Employee
                    BEGIN
                        DELETE FROM Employee_fts 
                        WHERE empID = old.empID;
                    END;''')

    cur.execute('''CREATE TRIGGER emp_fts_update AFTER UPDATE ON Employee
                    BEGIN
                        UPDATE Employee_fts
                        SET empID = new.empID,
                            empDep = new.empDep,
                            designation = (SELECT name FROM Designation 
                                            WHERE designationID IN (SELECT designationID 
                                                                    FROM EmployeeDesignation
                                                                    WHERE EmployeeDesignation.empID = new.empID)),
                            firstName = new.firstName,
                            lastName = new.lastName,
                            summary = new.summary
                        WHERE empID = old.empID;
                    END;''')

