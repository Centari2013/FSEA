from utils.authUtils import *
from utils.variables import *

# create new db (or open if already exists)
con = sqlite3.connect(db)

# create cursor for statement execution
cur = con.cursor()


# drop SpecimenMedical table from database if it exists
try:
    con.execute('''DROP TABLE SpecimenMedical''')
    con.commit()
    print('SpecimenMedical table dropped\n')

except:
    print('SpecimenMedical table does not exist\n')

# drop Origin table from database if it exists
try:
    con.execute('''DROP TABLE Origin''')
    con.commit()
    print('Origin table dropped\n')

except:
    print('Origin table does not exist\n')

# drop Mission table from database if it exists
try:
    con.execute('''DROP TABLE Mission''')
    con.commit()
    print('Mission table dropped\n')

except:
    print('Mission table does not exist\n')

# drop Specimen table from database if it exists
try:
    con.execute('''DROP TABLE Specimen''')
    con.commit()
    print('Specimen table dropped\n')

except:
    print('Specimen table does not exist\n')

# drop Credentials table from database if it exists
try:
    con.execute('DROP TABLE Credentials')
    con.commit()
    print('Credentials table dropped\n')

except:
    print('Credentials table does not exist\n')

# drop EmployeeMedical table from database if it exists
try:
    con.execute('''DROP TABLE EmployeeMedical''')
    con.commit()
    print('EmployeeMedical table dropped\n')

except:
    print('EmployeeMedical table does not exist\n')

# drop Employee table from database if it exists
try:
    con.execute('''DROP TABLE Employee''')
    con.commit()
    print('Employee table dropped\n')

except:
    print('Employee table does not exist\n')

# drop Department table from database if it exists
try:
    con.execute('DROP TABLE Department')
    con.commit()
    print('Department table dropped\n')

except:
    print('Department table does not exist\n')

# drop EmployeeSpecimen table from database if it exists
try:
    con.execute('''DROP TABLE EmployeeSpecimen''')
    con.commit()
    print('EmployeeSpecimen table dropped\n')

except:
    print('EmployeeSpecimen table does not exist\n')

# drop Department_fts table from database if it exists
try:
    con.execute('''DROP TABLE Department_fts''')
    con.commit()
    print('Department_fts table dropped\n')

except:
    print('Department_fts table does not exist\n')

# drop Employee_fts table from database if it exists
try:
    con.execute('''DROP TABLE Employee_fts''')
    con.commit()
    print('Employee_fts table dropped\n')

except:
    print('Employee_fts table does not exist\n')

# drop Specimen_fts table from database if it exists
try:
    con.execute('''DROP TABLE Specimen_fts''')
    con.commit()
    print('Specimen_fts table dropped\n')

except:
    print('Specimen_fts table does not exist\n')

# drop Origin_fts table from database if it exists
try:
    con.execute('''DROP TABLE Origin_fts''')
    con.commit()
    print('Origin_fts table dropped\n')

except:
    print('Origin_fts table does not exist\n')

# drop Mission_fts table from database if it exists
try:
    con.execute('''DROP TABLE Mission_fts''')
    con.commit()
    print('Mission_fts table dropped\n')

except:
    print('Mission_fts table does not exist\n')

# drop search_results table from database if it exists
try:
    con.execute('''DROP TABLE search_results''')
    con.commit()
    print('search_results table dropped\n')

except:
    print('search_results table does not exist\n')


# create Department table
cur.execute('''CREATE TABLE Department(
                depID           INTEGER UNIQUE NOT NULL,
                depName         TEXT NOT NULL,
                supervisorID    TEXT DEFAULT NULL,
                description     TEXT DEFAULT '',
                PRIMARY KEY (depID)
                );''')
con.commit()
print('Department table created\n')

# create Employee table in db
cur.execute('''CREATE TABLE Employee(
                empDep          INTEGER NOT NULL,
                empID           TEXT NOT NULL UNIQUE,
                designation     TEXT CHECK(designation IN {}) NOT NULL,
                firstName       TEXT CHECK(LENGTH(firstName) <= 50) NOT NULL,
                lastName        TEXT CHECK(LENGTH(lastName) <= 50)  NOT NULL,
                startDate       TEXT NOT NULL,
                endDate         TEXT DEFAULT NULL,
                summary         TEXT DEFAULT '',
                PRIMARY KEY (empID),
                FOREIGN KEY (empDep) REFERENCES Department(depId)
                );'''.format(designation))
# save changes
con.commit()
print('Employee table created\n')

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
# save changes
con.commit()
print('EmployeeMedical table created\n')

# create Credentials table
cur.execute('''CREATE TABLE Credentials(
                empID           TEXT NOT NULL UNIQUE,
                username        TEXT DEFAULT NULL,
                password        TEXT DEFAULT NULL,
                loginAttempts   INTEGER DEFAULT 0,
                PRIMARY KEY (empID),
                CONSTRAINT employeeID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE
                );''')
con.commit()
print('Credentials table created\n')

# create Origin table
cur.execute('''CREATE TABLE Origin(
                originID    TEXT NOT NULL UNIQUE,
                name        TEXT NOT NULL,
                missionID   TEXT DEFAULT 'MISSION-PENDING',
                description TEXT NOT NULL,
                PRIMARY KEY (originID)
                );''')
con.commit()
print('Origin table created\n')

cur.execute('''CREATE TABLE Mission(
                missionID       TEXT NOT NULL UNIQUE,
                name            TEXT NOT NULL,
                originID        TEXT DEFAULT 'ORIGIN-PENDING',
                startDate       TEXT DEFAULT NULL,
                endDate         TEXT DEFAULT NULL,
                captainID       TEXT DEFAULT NULL,
                supervisorID    TEXT DEFAULT NULL,
                description     TEXT NOT NULL,
                PRIMARY KEY (missionID),
                FOREIGN KEY (captainID) REFERENCES Employee(empID),
                FOREIGN KEY (supervisorID) REFERENCES Employee(empID)
                );''')
con.commit()
print('Mission table created\n')

cur.execute('''CREATE TABLE Specimen(
                specimenID              TEXT NOT NULL UNIQUE,
                name                    TEXT NOT NULL,
                origin                  TEXT DEFAULT NULL,
                missionID               TEXT DEFAULT NULL,
                threatLevel             REAL DEFAULT NULL,
                acquisitionDate         TEXT NOT NULL,
                notes                   TEXT DEFAULT NULL,
                description             TEXT DEFAULT '',
               PRIMARY KEY (specimenID),
               CONSTRAINT originID FOREIGN KEY (origin) REFERENCES Origin(originID) ON DELETE CASCADE,
               CONSTRAINT missionID FOREIGN KEY (missionID) REFERENCES Mission(missionID) ON DELETE CASCADE
               );''')
con.commit()
print('Specimen table created\n')

cur.execute('''CREATE TABLE EmployeeSpecimen(
                empID       TEXT NOT NULL,
                specimenID  TEXT NOT NULL,
               PRIMARY KEY (empID, specimenID),
               CONSTRAINT employeeID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE, 
               CONSTRAINT specimenID FOREIGN KEY (specimenID) REFERENCES Specimen(specimenID) ON DELETE CASCADE
               );''')
con.commit()
print('EmployeeSpecimen table created\n')

cur.execute('''CREATE TABLE SpecimenMedical(
                specimenID  TEXT NOT NULL,
                bloodtype   TEXT CHECK(bloodtype IN {}) DEFAULT NULL,
                sex         TEXT CHECK(sex IN {}) DEFAULT NULL,
                kilograms   REAL DEFAULT NULL,
                notes       TEXT DEFAULT NULL,
                PRIMARY KEY (specimenID),
                CONSTRAINT specimenID FOREIGN KEY (specimenID) REFERENCES Specimen(specimenID) ON DELETE CASCADE
                );'''.format(bloodtypes, sex))
con.commit()
print('SpecimenMedical table created\n')

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
con.commit()
print('Employee_fts table created\n')

cur.execute('''CREATE TRIGGER emp_inserts AFTER INSERT ON Employee
                BEGIN
                    INSERT INTO Employee_fts (empID, empDep, designation, firstName, lastName, summary)
                    VALUES (new.empID, new.empDep, new.designation, new.firstName, new.lastName, new.summary);
                    INSERT INTO EmployeeMedical(empID)
                    VALUES (new.empID); 
                    INSERT INTO Credentials (empID)
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
                        designation = new.designation,
                        firstName = new.firstName,
                        lastName = new.lastName,
                        summary = new.summary
                    WHERE empID = old.empID;
                END;''')
con.commit()


cur.execute('''CREATE VIRTUAL TABLE Specimen_fts USING fts5(
                specimenID, 
                name,
                origin,
                missionID, 
                threatLevel,
                acquisitionDate,
                notes,
                description,
                tokenize="porter"  
            )''')
con.commit()
print('Specimen_fts table created\n')

cur.execute('''CREATE TRIGGER specimen_inserts AFTER INSERT ON Specimen
                BEGIN
                    INSERT INTO Specimen_fts (specimenID, name, origin, missionID, threatLevel, acquisitionDate, notes, description)
                    VALUES (new.specimenID, new.name, new.origin, new.missionID, new.threatLevel, new.acquisitionDate, new.notes, new.description);
                    INSERT INTO SpecimenMedical (specimenID)
                    VALUES (new.specimenID);
                END;''')

cur.execute('''CREATE TRIGGER specimen_fts_delete AFTER DELETE ON Specimen
                BEGIN
                    DELETE FROM Specimen_fts
                    WHERE specimenID = old.specimenID;
                END;''')

cur.execute('''CREATE TRIGGER specimen_fts_update AFTER UPDATE ON Specimen
                BEGIN
                    UPDATE Specimen_fts
                    SET specimenID = new.specimenID,
                        name = new.name,
                        origin = new.origin,
                        missionID = new.missionID,
                        threatLevel = new.threatLevel,
                        acquisitionDate = new.acquisitionDate,
                        notes = new.notes,
                        description = new.description
                    WHERE specimenID = old.specimenID;
                    UPDATE SpecimenMedical
                    SET specimenID = new.specimenID
                    WHERE specimenID = old.specimenID;
                END;''')
con.commit()


cur.execute('''CREATE VIRTUAL TABLE Department_fts USING fts5(
                depID,
                depName,
                supervisorID,
                description,
                tokenize="porter"  
            )''')
con.commit()
print('Department_fts table created\n')

cur.execute('''CREATE TRIGGER department_fts_insert AFTER INSERT ON Department
                BEGIN
                    INSERT INTO Department_fts (depID, depName, supervisorID, description)
                    VALUES (new.depID, new.depName, new.supervisorID, new.description);
                END;''')

cur.execute('''CREATE TRIGGER department_fts_delete AFTER DELETE ON Department
                BEGIN
                    DELETE FROM Department_fts 
                    WHERE depID = old.depID;
                END;''')

cur.execute('''CREATE TRIGGER department_fts_update AFTER UPDATE ON Department
                BEGIN
                    UPDATE Department_fts
                    SET depID = new.depID, 
                        depName = new.depName, 
                        supervisorID = new.supervisorID, 
                        description = new.description
                    WHERE depID = old.depID;
                END;''')
con.commit()


cur.execute('''CREATE VIRTUAL TABLE Origin_fts USING fts5(
                originID,
                name,
                missionID,
                description,
                tokenize="porter"  
            )''')
con.commit()
print('Origin_fts table created\n')

cur.execute('''CREATE TRIGGER origin_fts_insert AFTER INSERT ON Origin
                BEGIN
                    INSERT INTO Origin_fts (originID, name, missionID, description)
                    VALUES (new.originID, new.name, new.missionID, new.description);
                END;''')

cur.execute('''CREATE TRIGGER origin_fts_delete AFTER DELETE ON Origin
                BEGIN
                    DELETE FROM Origin_fts 
                    WHERE originID = old.originID;
                END;''')

cur.execute('''CREATE TRIGGER origin_fts_update AFTER UPDATE ON Origin
                BEGIN
                    UPDATE Origin_fts
                    SET originID = new.originID,
                        name = new.name,
                        missionID = new.missionID,
                        description = new.description
                    WHERE originID = old.originID;
                END;''')
con.commit()


cur.execute('''CREATE VIRTUAL TABLE Mission_fts USING fts5(
                missionID,
                name,
                originID,
                startDate UNINDEXED,
                endDate UNINDEXED,
                captainID,
                supervisorID,
                description,
                tokenize="porter"  
            )''')
con.commit()
print('Mission_fts table created\n')

cur.execute('''CREATE TRIGGER mission_fts_insert AFTER INSERT ON Mission
                BEGIN
                    INSERT INTO Mission_fts (missionID, name, originID, startDate, endDate, captainID, supervisorID, description)
                    VALUES (new.missionID, new.name, new.originID, new.startDate, new.endDate, new.captainID, new.supervisorID, new.description);
                END;''')

cur.execute('''CREATE TRIGGER mission_fts_delete AFTER DELETE ON Mission
                BEGIN
                    DELETE FROM Mission_fts
                    WHERE missionID = old.missionID;
                END;''')

cur.execute('''CREATE TRIGGER mission_fts_update AFTER UPDATE ON Mission
                BEGIN
                    UPDATE Mission_fts
                    SET missionID = new.missionID,
                        name = new.name,
                        originID = new.originID,
                        startDate = new.startDate,
                        endDate = new.endDate, 
                        captainID = new.captainID,
                        supervisorID = new.supervisorID,
                        description = new.description
                    WHERE missionID = old.missionID;
                END;''')
con.commit()

cur.execute('''CREATE TABLE search_results(
                        type        TEXT,
                        id          TEXT,
                        firstName   TEXT,
                        lastName    TEXT,
                        description TEXT,
                        rank        INTEGER
                        );''')
con.commit()

con.close()
