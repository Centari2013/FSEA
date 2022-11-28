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

# create Department table
cur.execute('''CREATE TABLE Department(
                depID           INTEGER,
                depName         TEXT NOT NULL,
                supervisorID    TEXT DEFAULT NULL,
                description     TEXT DEFAULT NULL,
                PRIMARY KEY (depID)
                );''')
con.commit()
print('Department table created\n')

# create Employee table in db
cur.execute('''CREATE TABLE Employee( 
                id              INTEGER,
                empDep          INTEGER NOT NULL,
                empID           TEXT NOT NULL UNIQUE,
                designation     TEXT CHECK(designation IN {}) NOT NULL,
                firstName       TEXT CHECK(LENGTH(firstName) <= 50) NOT NULL,
                lastName        TEXT CHECK(LENGTH(lastName) <= 50)  NOT NULL,
                startDate       TEXT NOT NULL,
                endDate         TEXT DEFAULT NULL,
                PRIMARY KEY (id),
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
                notes           TEXT DEFAULT NULL,
                PRIMARY KEY (empID),
                CONSTRAINT  empID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE
                );'''.format(bloodtypes, sex))
# save changes
con.commit()
print('EmployeeMedical table created\n')

# create Credentials table
cur.execute('''CREATE TABLE Credentials(
                empID           TEXT NOT NULL UNIQUE,
                username        TEXT NOT NULL,
                password        TEXT NOT NULL,
                loginAttempts   INTEGER DEFAULT 0,
                PRIMARY KEY (empID),
                CONSTRAINT employeeID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE
                );''')
con.commit()
print('Credentials table created')

# create Origin table
cur.execute('''CREATE TABLE Origin(
                id          INTEGER,
                originID    TEXT NOT NULL UNIQUE,
                name        TEXT NOT NULL,
                missionID   TEXT DEFAULT 'MISSION-PENDING',
                description TEXT NOT NULL,
                PRIMARY KEY (id)
                );''')
con.commit()

cur.execute('''CREATE TABLE Mission(
                id              INTEGER,
                missionID       TEXT NOT NULL UNIQUE,
                name            TEXT NOT NULL,
                originID        TEXT DEFAULT 'ORIGIN-PENDING',
                startDate       TEXT DEFAULT NULL,
                endDate         TEXT DEFAULT NULL,
                captainID       TEXT DEFAULT NULL,
                supervisorID    TEXT DEFAULT NULL,
                description     TEXT NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (captainID) REFERENCES Employee(empID),
                FOREIGN KEY (supervisorID) REFERENCES Employee(empID)
                );''')
con.commit()

cur.execute('''CREATE TABLE Specimen(
                id                      INTEGER,
                specimenID              TEXT NOT NULL UNIQUE,
                name                    TEXT NOT NULL,
                origin                  TEXT DEFAULT 'unknown',
                mission                 TEXT DEFAULT 'N/A',
                threatLevel             REAL DEFAULT NULL,
                acquisitionDate         TEXT NOT NULL,
                notes                   TEXT DEFAULT NULL,
               PRIMARY KEY (id),
               CONSTRAINT originID FOREIGN KEY (origin) REFERENCES Origin(originID) ON DELETE CASCADE,
               CONSTRAINT missionID FOREIGN KEY (mission) REFERENCES Mission(missionID) ON DELETE CASCADE
               );''')
con.commit()

cur.execute('''CREATE TABLE EmployeeSpecimen(
                empID       TEXT NOT NULL,
                specimenID  TEXT NOT NULL,
               PRIMARY KEY (empID, specimenID),
               CONSTRAINT employeeID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE, 
               CONSTRAINT specimenID FOREIGN KEY (specimenID) REFERENCES Specimen(specimenID) ON DELETE CASCADE
               );''')
con.commit()

cur.execute('''CREATE TABLE SpecimenMedical(
                specimenID  TEXT NOT NULL,
                bloodtype   TEXT CHECK(bloodtype IN {}),
                sex         TEXT CHECK(sex IN {}) DEFAULT NULL,
                kilograms   REAL DEFAULT NULL,
                notes       TEXT DEFAULT NULL,
                PRIMARY KEY (specimenID),
                CONSTRAINT specimenID FOREIGN KEY (specimenID) REFERENCES Specimen(specimenID) ON DELETE CASCADE
                );'''.format(bloodtypes, sex))
con.commit()


con.close()
