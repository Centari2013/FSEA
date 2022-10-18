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
    print('Department table dropped')

except:
    print('Department table does not exist')

# drop Employee table from database if it exists
try:
    con.execute('''DROP TABLE Employee''')
    con.commit()
    print('Employee table dropped')

except:
    print('Employee table does not exist.')

# drop Credentials table from database if it exists
try:
    con.execute('DROP TABLE Credentials')
    con.commit()
    print("Credentials table dropped")

except:
    print("Credentials table does not exist")

# create Department table
cur.execute('''CREATE TABLE Department(
                depID       INT NOT NULL,
                depName     TEXT NOT NULL,
                description TEXT,
                PRIMARY KEY (depID)
                );''')
con.commit()

# create Employee table in db
cur.execute('''CREATE TABLE Employee( 
                empDep          INT NOT NULL,
                empID           TEXT NOT NULL,
                designation     TEXT CHECK(designation IN ('ADMIN','CP', 'ELEC-ENG', 'PLAN-GEO', 'MECH-ENG', 'CHEM')),
                firstName       TEXT CHECK(LENGTH(firstName) <= 50) NOT NULL,
                lastName        TEXT CHECK(LENGTH(lastName) <= 50)  NOT NULL,
                PRIMARY KEY (empID),
                FOREIGN KEY (empDep) REFERENCES Department(depId)
                );''')

# save changes
con.commit()
print('Employee table created.')

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

# insert departments
departments = [(1, 'ZERO'),
              (2, 'EXEC')]
cur.executemany('INSERT INTO Department (depID, depName) VALUES(?, ?);', departments)
con.commit()
print('Data inserted into Department Table')

employees = [(1, '', 'CP', 'Prisca', 'Poteau'),
             (1, '', 'ELEC-ENG', 'Revy',     'Sagan'),
             (1, '', 'CHEM',     'Michael',  'Lowe')]

employees = [list(row) for row in employees]

# generate random empID for each employee
for row in employees:
    uid = generateUID()
    print(uid)
    cur.execute('SELECT empID FROM Employee WHERE empID = ?', [uid])
    query = cur.fetchone()

    while query is not None:
        uid = generateUID()
        cur.execute('SELECT empID FROM Employee WHERE empID = ?', [uid])
        query = cur.fetchone()

    row[1] = uid
    # encrypt first name
    row[3] = str(encryption.cipher.encrypt(bytes(row[3], 'utf-8')).decode('utf-8'))
    # encrypt last name
    row[4] = str(encryption.cipher.encrypt(bytes(row[4], 'utf-8')).decode('utf-8'))


employees = [tuple(row) for row in employees]


# populate Employee table
cur.executemany('INSERT INTO Employee VALUES(?,?,?,?,?);', employees)
con.commit()
print('Data inserted into Employee table.')

# populate Credentials table
cur.execute('SELECT empID FROM Employee;')
query = cur.fetchall()
# convert list of tuples to list of strings
query = ['%s' % item for item in query]


for e in query:
    username = generateUsername(e)
    password = str(encryption.cipher.encrypt(bytes(generatePWD(), 'utf-8')).decode('utf-8'))

    cur.execute('INSERT INTO Credentials (empID, username, password) VALUES(?, ?, ?)', (e, username, password))

con.commit()
print('Data inserted into Credentials table')

deptNum = 2
idNum = '00000000'
designation = 'ADMIN'
firstName = b'Zaria'
lastName = b'Burton'
username = b'zburton_ADMIN'
password = b'admin'
loginAttempts = 0

firstName = str(encryption.cipher.encrypt(firstName).decode('utf-8'))
lastName = str(encryption.cipher.encrypt(lastName).decode('utf-8'))
username = str(encryption.cipher.encrypt(username).decode('utf-8'))
password = str(encryption.cipher.encrypt(password).decode('utf-8'))

admin = (deptNum, idNum, designation, firstName, lastName)
creds = (idNum, username, password, loginAttempts)

cur.execute('INSERT INTO Employee VALUES (?,?,?,?,?)', admin)
con.commit()
cur.execute('INSERT INTO Credentials VALUES (?,?,?,?)', creds)
con.commit()
print('admin credentials added')

# iterate over rows in table
print('Department Table')
for row in cur.execute('SELECT * FROM Department;'):
    print(row)
print('\n')

print('Employee Table')
for row in cur.execute('SELECT * FROM Employee;'):
    print(row)
print('\n')

print('Credentials Table')
for row in cur.execute('SELECT * FROM Credentials;'):
    row = list(row)
    row[1] = str(encryption.cipher.decrypt(bytes(row[1], 'utf-8')).encode('utf-8').decode('utf-8'))
    row[2] = str(encryption.cipher.decrypt(bytes(row[2], 'utf-8')).encode('utf-8').decode('utf-8'))
    print(row)

con.close()
print('Connection closed.')
