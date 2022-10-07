import sqlite3
from utils import authUtils, encryption

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
# TODO implement login attempt counter
cur.execute('''create table Employee( 
                empDep          TEXT CHECK(empDep IN ('SPEC-OP', 'EX-HEAD')),
                empID           TEXT NOT NULL,
                designation     TEXT CHECK(designation IN ('CP', 'ELEC-ENG', 'PLAN-GEO', 'MECH-ENG', 'CHEM')),
                firstName       TEXT CHECK(LENGTH(firstName) <= 50) NOT NULL,
                lastName        TEXT CHECK(LENGTH(lastName) <= 50)  NOT NULL,
                username        TEXT NOT NULL,
                password        TEXT NOT NULL,
                PRIMARY KEY (empID)
                );''')

# save changes
con.commit()
print('Employee table created.')

data = [('SPEC-OP', '', 'CP',       'Prisca',   'Poteau', 'ppoteau_cp',     'poop'),
        ('SPEC-OP', '', 'ELEC-ENG', 'Revy',     'Sagan',  'rsagan_eleceng', authUtils.generatePWD()),
        ('SPEC-OP', '', 'CHEM',     'Michael',  'Lowe',   'mlowe_chem',     authUtils.generatePWD())]

data = [list(row) for row in data]

for row in data:
    uid = authUtils.generateUID()
    cur.execute('select empID from Employee where empID = ?', [uid])
    query = cur.fetchone()
    while query is not None:
        uid = authUtils.generateUID()
        cur.execute('select empID from Employee where empID = ?', [uid])
        query = cur.fetchone()
    row[1] = str(encryption.cipher.encrypt(bytes(uid, 'utf-8')).decode('utf-8'))
    row[3] = str(encryption.cipher.encrypt(bytes(row[3], 'utf-8')).decode('utf-8'))
    row[4] = str(encryption.cipher.encrypt(bytes(row[4], 'utf-8')).decode('utf-8'))
    row[5] = str(encryption.cipher.encrypt(bytes(row[5], 'utf-8')).decode('utf-8'))
    row[6] = str(encryption.cipher.encrypt(bytes(row[6], 'utf-8')).decode('utf-8'))

data = [tuple(row) for row in data]

# populate table
cur.executemany('insert into Employee values(?,?,?,?,?,?,?);', data)
con.commit()
print('Data inserted into Employee table.')

# iterate over rows in table
for row in cur.execute('select * from Employee;'):
    print(row)

con.close()
print('Connection closed.')
