import datetime
import sqlite3
from utils.encryption import *
from utils.authUtils import *

# create new db (or open if already exists)
con = sqlite3.connect('FSEA.db')

# create cursor for statement execution
cur = con.cursor()

# drop Department table from database if it exists
try:
    con.execute('DROP TABLE Department')
    con.commit()
    print('Department table dropped\n')

except:
    print('Department table does not exist\n')

# drop Employee table from database if it exists
try:
    con.execute('''DROP TABLE Employee''')
    con.commit()
    print('Employee table dropped\n')

except:
    print('Employee table does not exist\n')

# drop EmployeeMedical table from database if it exists
try:
    con.execute('''DROP TABLE EmployeeMedical''')
    con.commit()
    print('EmployeeMedical table dropped\n')

except:
    print('EmployeeMedical table does not exist\n')

# drop Credentials table from database if it exists
try:
    con.execute('DROP TABLE Credentials')
    con.commit()
    print('Credentials table dropped\n')

except:
    print('Credentials table does not exist\n')

# create Department table
cur.execute('''CREATE TABLE Department(
                depID           INT NOT NULL,
                depName         TEXT NOT NULL,
                supervisorID    TEXT DEFAULT NULL,
                description     TEXT,
                PRIMARY KEY (depID)
                );''')
con.commit()
print('Department table created')

# insert departments
departments = [(1, 'ZERO'),
              (2, 'EXEC')]
cur.executemany('INSERT INTO Department (depID, depName) VALUES(?, ?);', departments)
con.commit()
print('Data inserted into Department table\n')


# create Employee table in db
cur.execute('''CREATE TABLE Employee( 
                empDep          INT NOT NULL,
                empID           TEXT NOT NULL,
                designation     TEXT CHECK(designation IN ('ADMIN','CP', 'ENG', 'GEO', 'CHEM', 'SUPER', 'TECH', 'SOLDIER', 'BIO')),
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
                bloodtype       TEXT CHECK(bloodtype IN ('A+', 'O+', 'B+', 'AB+', 'A-', 'O-', 'B-', 'AB-', 'V-', 'V+', 'BF', 'undefined')) NOT NULL,
                sex             TEXT CHECK(sex IN ('male', 'female', 'inter', 'unknown','undefined')) NOT NULL,
                kilograms       REAL DEFAULT NULL,
                height          REAL DEFAULT NULL,
                notes           TEXT DEFAULT NULL,
                PRIMARY KEY (empID),
                FOREIGN KEY (empID) REFERENCES Employee(empID)
                );''')
# save changes
con.commit()
print('EmployeeMedical table created\n')

employees = [[1, '', 'CP',      'Prisca',   'Poteau',   datetime.date(2071, 9, 19),     None],
             [1, '', 'ENG',     'Revy',     'Sagan',    datetime.date(2072, 6, 30),     None],
             [1, '', 'CHEM',    'Michael',  'Lowe',     datetime.date(2056, 7, 25),     None],
             [1, '', 'ENG',     'Benjamin', 'Colson',   datetime.date(2047, 4, 15),     None],
             [1, '', 'BIO',     'Mingmei',  'Gao',      datetime.date(2061, 12, 3),     None],
             [1, '', 'GEO',     'Abdul',    'Said',     datetime.date(2061, 12, 3),     None],
             [1, '', 'SUPER',   'Historia', 'Lowe',     datetime.date(2038, 1, 31),     None],
             [2, '', 'SUPER',   'Jurio',    'Caldero',  datetime.date(2042, 6, 30),     None],
             [1, '', 'SOLDIER', 'Joseph',   'Smith',    datetime.date(2060, 11, 12),    None],
             [2, '', 'SUPER',   'Markus',   'Belcost',  datetime.date(2067, 6, 8),      None],
             [2, '', 'SOLDIER', 'Aurelis',  'Dreymond', datetime.date(2075, 12, 13),    None],
             [2, '', 'SOLDIER', 'Quani',    'Dreymond', datetime.date(2075, 12, 13),    None],
             [1, '', 'TECH',    'Daryl',    'Belcost',  datetime.date(2071, 3, 16),     None]]

medicalData = [['', datetime.date(2052, 10, 15),    'undefined',    'female',   85.3,   177.8,  None],
               ['', datetime.date(2053, 3, 7),      'V-',           'female',   75.7,   158.75, 'monitoring hemochromia'],
               ['', datetime.date(2040, 7, 24),     'B+',           'male',     87.1,   182.88, '8th regen cycle'],
               ['', datetime.date(2019, 9, 22),     'O+',           'inter',    95.3,   177.8,  None],
               ['', datetime.date(2038, 5, 9),      'AB+',          'female',   59.9,   166.37, 'pregnant'],
               ['', datetime.date(2041, 5, 9),      'A+',           'male',     78.5,   185.42, None],
               ['', datetime.date(2024, 12, 25),    'AB-',          'female',   70.3,   170.18, '3rd regen cycle'],
               ['', datetime.date(2022, 9, 1),      'A-',           'male',     88.5,   186.69, '2nd regen cycle'],
               ['', datetime.date(2042, 5, 15),     'O-',           'male',     90.7,   175.26, None],
               ['', datetime.date(2052, 1, 1),      'undefined',    'male',     72.1,   473.99, 'dormant massimonia'],
               ['', None,                           'undefined',    'female',   81.6,   186.69, None],
               ['', None,                           'undefined',    'female',   77.6,   177.8,  None],
               ['', None,                           'BF',           'male',     113.4,  180.34, 'has gained sentience']]

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

    data = medicalData[i][6]
    if data is not None:
        medicalData[i][6] = str(encryption.cipher.encrypt(bytes(medicalData[i][6], 'utf-8')).decode('utf-8'))


employees = [tuple(row) for row in employees]
medicalData = [tuple(row) for row in medicalData]

# populate Employee table & EmployeeMedical table
cur.executemany('INSERT INTO Employee VALUES(?,?,?,?,?,?,?);', employees)
con.commit()
print('Data inserted into Employee table\n')
cur.executemany('INSERT INTO EmployeeMedical VALUES(?,?,?,?,?,?,?);', medicalData)
con.commit()
print('Data inserted into EmployeeMedical table\n')


# populate EmployeeMedical table


cur.execute('SELECT empID FROM Employee;')
query = cur.fetchall()
# convert list of tuples to list of strings
query = ['%s' % item for item in query]


# create Credentials table
cur.execute('''CREATE TABLE Credentials( 
                empID           TEXT NOT NULL,
                username        TEXT NOT NULL,
                password        TEXT NOT NULL,
                loginAttempts   INT DEFAULT 0,
                PRIMARY KEY (empID),
                CONSTRAINT employeeID
                    FOREIGN KEY (empID)
                    REFERENCES Employee(empID)
                    ON DELETE CASCADE
                );''')
con.commit()
print('Credentials table created')

for e in query:
    username = generateUsername(e)
    password = str(encryption.cipher.encrypt(bytes(generatePWD(), 'utf-8')).decode('utf-8'))

    cur.execute('INSERT INTO Credentials (empID, username, password) VALUES(?, ?, ?)', (e, username, password))

con.commit()
print('Data inserted into Credentials table\n')

# insert admin data
deptNum = 2
idNum = '00000000'
designation = 'ADMIN'
firstName = b'Zaria'
lastName = b'Burton'
username = b'admin'
password = b'admin'
loginAttempts = 0

firstName = str(encryption.cipher.encrypt(firstName).decode('utf-8'))
lastName = str(encryption.cipher.encrypt(lastName).decode('utf-8'))
username = str(encryption.cipher.encrypt(username).decode('utf-8'))
password = str(encryption.cipher.encrypt(password).decode('utf-8'))

admin = (deptNum, idNum, designation, firstName, lastName, datetime.date(2022, 10, 27))
creds = (idNum, username, password, loginAttempts)

cur.execute('INSERT INTO Employee VALUES (?,?,?,?,?,?,NULL)', admin)
con.commit()
cur.execute('INSERT INTO Credentials VALUES (?,?,?,?)', creds)
con.commit()
print('Admin credentials added')

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
    #row[1] = str(encryption.cipher.decrypt(bytes(row[1], 'utf-8')).encode('utf-8').decode('utf-8'))
    #row[2] = str(encryption.cipher.decrypt(bytes(row[2], 'utf-8')).encode('utf-8').decode('utf-8'))
    print(row)

con.close()
print('Database connection closed.')
