import sqlite3
from utils import authUtils

# create new db (or open if already exists)
con = sqlite3.connect('FSEA.db')

# create cursor for statement execution
cur = con.cursor()

# drop Employee table from database if exists
try:
    con.execute('''Drop table Employee''')
    con.commit()
    print("Employee table dropped")

except:
    print("Employee table does not exist.")

# create Employee table in db
# TODO add CHECK constraints
cur.execute('''create table Employee( 
                empDep          TEXT CHECK(empDep IN ('SPEC-OP', 'EX-HEAD')),
                empID           TEXT CHECK(LENGTH(empID) == 8) NOT NULL,
                designation     TEXT CHECK(designation IN ('CP', 'ELEC-ENG', 'PLAN-GEO', 'MECH-ENG', 'CHEM')),
                firstName       TEXT CHECK(LENGTH(firstName) <= 50) NOT NULL,
                lastName        TEXT CHECK(LENGTH(lastName) <= 50)  NOT NULL,
                password        TEXT CHECK(LENGTH(password) >= 8)   NOT NULL,
                PRIMARY KEY (empDep, empID)
                );''')

# save changes
con.commit()
print('Employee table created.')

data = [('SPEC-OP', '', 'CP', 'Prisca', 'Poteau', authUtils.generatePWD()),
        ('SPEC-OP', '', 'ELEC-ENG', 'Revy', 'Sagan', authUtils.generatePWD()),
        ('SPEC-OP', '', 'CHEM', 'Michael', 'Lowe', authUtils.generatePWD())]

data = [list(row) for row in data]

for row in data:
    uid = authUtils.generateUID()
    cur.execute('select empID from Employee where empID = ?', [uid])
    query = cur.fetchone()
    while query is not None:
        uid = authUtils.generateUID()
        cur.execute('select empID from Employee where empID = ?', [uid])
        query = cur.fetchone()
    row[1] = uid
    print("UID: ", uid)

data = [tuple(row) for row in data]

# populate table
cur.executemany('insert into Employee values(?,?,?,?,?,?);', data)
con.commit()
print('Data inserted into Employee table.')

# iterate over rows in table
for row in cur.execute('select * from Employee;'):
    print(row)

con.close()
print('Connection closed.')
