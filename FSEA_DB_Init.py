import datetime
import sqlite3
from utils.encryption import *
from utils.variables import db
from utils.authUtils import *

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
                depID           INT NOT NULL,
                depName         TEXT NOT NULL,
                supervisorID    TEXT DEFAULT NULL,
                description     TEXT DEFAULT NULL,
                PRIMARY KEY (depID)
                );''')
con.commit()
print('Department table created')

# create Employee table in db
cur.execute('''CREATE TABLE Employee( 
                empDep          INT NOT NULL,
                empID           TEXT NOT NULL,
                designation     TEXT CHECK(designation IN ('ADMIN','CP', 'ENG', 'GEO', 'CHEM', 'SUPER', 'TECH', 'SOLDIER', 'BIO')) NOT NULL,
                firstName       TEXT CHECK(LENGTH(firstName) <= 50) NOT NULL,
                lastName        TEXT CHECK(LENGTH(lastName) <= 50)  NOT NULL,
                startDate       TEXT NOT NULL,
                endDate         TEXT DEFAULT NULL,
                PRIMARY KEY (empID),
                FOREIGN KEY (empDep) REFERENCES Department(depId)
                );''')
# save changes
con.commit()
print('Employee table created\n')

# create EmployeeMedical table in db
cur.execute('''CREATE TABLE EmployeeMedical( 
                empID           TEXT NOT NULL,
                dob             TEXT DEFAULT NULL,
                bloodtype       TEXT CHECK(bloodtype IN ('A+', 'O+', 'B+', 'AB+', 'A-', 'O-', 'B-', 'AB-', 'V-', 'V+', 'BF', 'undefined')),
                sex             TEXT CHECK(sex IN ('male', 'female', 'inter', 'unknown','undefined')),
                kilograms       REAL DEFAULT NULL,
                height          REAL DEFAULT NULL,
                notes           TEXT DEFAULT NULL,
                PRIMARY KEY (empID),
                CONSTRAINT  empID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE
                );''')
# save changes
con.commit()
print('EmployeeMedical table created\n')

# create Credentials table
cur.execute('''CREATE TABLE Credentials( 
                empID           TEXT NOT NULL,
                username        TEXT NOT NULL,
                password        TEXT NOT NULL,
                loginAttempts   INT DEFAULT 0,
                PRIMARY KEY (empID),
                CONSTRAINT employeeID FOREIGN KEY (empID) REFERENCES Employee(empID) ON DELETE CASCADE
                );''')
con.commit()
print('Credentials table created')

# create Origin table
cur.execute('''CREATE TABLE Origin(
                originID    TEXT NOT NULL,
                name        TEXT NOT NULL,
                missionID   TEXT DEFAULT 'MISSION-PENDING',
                description TEXT NOT NULL,
                PRIMARY KEY (originID)
                );''')
con.commit()

cur.execute('''CREATE TABLE Mission(
                missionID       TEXT NOT NULL,
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

cur.execute('''CREATE TABLE Specimen(
                specimenID  TEXT NOT NULL,
                name        TEXT NOT NULL,
                origin      TEXT DEFAULT 'unknown',
                mission     TEXT DEFAULT 'N/A',
                threatLevel REAL DEFAULT NULL,
                dob         TEXT DEFAULT 'unknown',
                notes       TEXT DEFAULT NULL,
               PRIMARY KEY (specimenID),
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
                bloodtype   TEXT CHECK(bloodtype IN ('A+', 'O+', 'B+', 'AB+', 'A-', 'O-', 'B-', 'AB-', 'V-', 'V+', 'BF', 'undefined')),
                sex         TEXT CHECK(sex IN ('male', 'female', 'inter', 'unknown','undefined')) NOT NULL,
                kilograms   REAL DEFAULT NULL,
                notes       TEXT DEFAULT NULL,
                CONSTRAINT specimenID FOREIGN KEY (specimenID) REFERENCES Specimen(specimenID) ON DELETE CASCADE
                );''')

con.create_function('username_gen', 3, generateUsername)
con.create_function('pwd_gen', 0, generatePWD)
con.commit()

con.execute('''CREATE TRIGGER IF NOT EXISTS employeeSetup 
                    AFTER INSERT 
                    ON Employee
                BEGIN
                    
                    INSERT INTO EmployeeMedical (empID) VALUES (NEW.empID);
                    INSERT INTO Credentials (empID, username, password) 
                        VALUES (NEW.empID, username_gen(NEW.firstName, NEW.lastName, NEW.designation), pwd_gen());
                END;''')


''''''''''INSERTS'''''''''

# insert departments
departments = [(1, 'ZERO'),
               (2, 'EXEC')]
cur.executemany('INSERT INTO Department (depID, depName) VALUES(?, ?);', departments)
con.commit()
print('Data inserted into Department table\n')

employees = [[1, '', 'CP', 'Prisca', 'Poteau', datetime.date(2071, 9, 19)],
             [1, '', 'ENG', 'Revy', 'Sagan', datetime.date(2072, 6, 30)],
             [1, '', 'CHEM', 'Michael', 'Lowe', datetime.date(2056, 7, 25)],
             [1, '', 'ENG', 'Benjamin', 'Colson', datetime.date(2047, 4, 15)],
             [1, '', 'BIO', 'Mingmei', 'Gao', datetime.date(2061, 12, 3)],
             [1, '', 'GEO', 'Abdul', 'Said', datetime.date(2061, 12, 3)],
             [1, '', 'SUPER', 'Historia', 'Lowe', datetime.date(2038, 1, 31)],
             [2, '', 'SUPER', 'Jurio', 'Caldero', datetime.date(2042, 6, 30)],
             [1, '', 'SOLDIER', 'Joseph', 'Smith', datetime.date(2060, 11, 12)],
             [2, '', 'SUPER', 'Markus', 'Belcost', datetime.date(2067, 6, 8)],
             [2, '', 'SOLDIER', 'Aurelis', 'Dreymond', datetime.date(2075, 12, 13)],
             [2, '', 'SOLDIER', 'Quani', 'Dreymond', datetime.date(2075, 12, 13)],
             [1, '', 'TECH', 'Daryl', 'Belcost', datetime.date(2071, 3, 16)]]

medicalData = [['', datetime.date(2052, 10, 15), 'undefined', 'female', 85.3, 177.8],
               ['', datetime.date(2053, 3, 7), 'V-', 'female', 75.7, 158.75, 'monitoring hemochromia'],
               ['', datetime.date(2040, 7, 24), 'B+', 'male', 87.1, 182.88, '8th regen cycle'],
               ['', datetime.date(2019, 9, 22), 'O+', 'inter', 95.3, 177.8],
               ['', datetime.date(2038, 5, 9), 'AB+', 'female', 59.9, 166.37, 'pregnant'],
               ['', datetime.date(2041, 5, 9), 'A+', 'male', 78.5, 185.42],
               ['', datetime.date(2024, 12, 25), 'AB-', 'female', 70.3, 170.18, '3rd regen cycle'],
               ['', datetime.date(2022, 9, 1), 'A-', 'male', 88.5, 186.69, '2nd regen cycle'],
               ['', datetime.date(2042, 5, 15), 'O-', 'male', 90.7, 175.26],
               ['', datetime.date(2052, 1, 1), 'undefined', 'male', 72.1, 473.99, 'dormant massimonia'],
               ['', 'undefined', 'female', 81.6, 186.69],
               ['', 'undefined', 'female', 77.6, 177.8],
               ['', 'BF', 'male', 113.4, 180.34, 'has gained sentience']]

# generate random empID for each employee
for i in range(len(employees)):
    uid = generateUID()
    cur.execute('SELECT empID FROM Employee WHERE empID = ?', [uid])
    query = cur.fetchone()

    while query is not None:
        uid = generateUID()
        cur.execute('SELECT empID FROM Employee WHERE empID = ?', [uid])
        query = cur.fetchone()

    employees[i][1] = uid
    # encrypt first name
    employees[i][3] = str(encryption.cipher.encrypt(bytes(employees[i][3], 'utf-8')).decode('utf-8'))
    # encrypt last name
    employees[i][4] = str(encryption.cipher.encrypt(bytes(employees[i][4], 'utf-8')).decode('utf-8'))

    medicalData[i][0] = uid

    if len(medicalData[i]) > 6:
        medicalData[i][6] = str(encryption.cipher.encrypt(bytes(medicalData[i][6], 'utf-8')).decode('utf-8'))

employees = [tuple(row) for row in employees]
medicalData = [tuple(row) for row in medicalData]

# populate Employee table & EmployeeMedical table
cur.executemany('INSERT INTO Employee(empDep, empID, designation, firstName, lastName, startDate) VALUES(?,?,?,?,?,?);',
                employees)


con.commit()

# origin and mission data
origins = [[generateUID(), 'Lypso', b'highly hazardous gaseous ice planet']]
missions = [[generateUID(), 'Dying Prophet', origins[0][0], None, None, None, None,
             b'recon for reports of glowing \'rosetta-stone-like\' object']]
origins[0][2] = str(encryption.cipher.encrypt(origins[0][2]).decode('utf-8'))
missions[0][7] = str(encryption.cipher.encrypt(missions[0][7]).decode('utf-8'))

origins = [tuple(r) for r in origins]
missions = [tuple(r) for r in missions]

cur.executemany('INSERT INTO Origin(originID, name, description) VALUES(?,?,?)', origins)
con.commit()
print('Data inserted into Origin table')
cur.executemany('INSERT INTO Mission VALUES(?,?,?,?,?,?,?,?)', missions)
con.commit()
print('Data inserted into Mission table')

cur.execute('''UPDATE Origin
                SET missionID = (SELECT missionID
                                    FROM Mission
                                   WHERE originID = Origin.originID
           )''')

cur.execute('INSERT INTO Specimen(specimenID, name, notes) VALUES(?,?,?)',
            (generateUID(), 'Massimo', 'member of department 0'))

# iterate over rows in table
print('Department Table')
for row in cur.execute('SELECT * FROM Department;'):
    print(row)
print('\n')

print('Employee Table')
for row in cur.execute('SELECT * FROM Employee;'):
    print(row)
print('\n')

print('EmployeeMedical Table')
for row in cur.execute('SELECT * FROM EmployeeMedical;'):
    print(row)
print('\n')

print('Credentials Table')
for row in cur.execute('SELECT * FROM Credentials;'):
    row = list(row)
    print(row)
print('\n')

print('Origin Table')
for row in cur.execute('SELECT * FROM Origin;'):
    row = list(row)
    print(row)
print('\n')

print('Mission Table')
for row in cur.execute('SELECT * FROM Mission;'):
    row = list(row)
    print(row)
print('\n')

con.close()
print('Database connection closed.')
