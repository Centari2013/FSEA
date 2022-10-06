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
cur.execute('''create table Employee( 
                empDep          ENUM('SPEC-OP', 'EX-HEAD'),
                empID           TEXT NOT NULL,
                designation     ENUM('CP', 'ELEC-ENG', 'PLAN-GEO', 'MECH-ENG'),
                FirstName       TEXT NOT NULL,
                LastName        TEXT NOT NULL,
                username        TEXT NOT NULL,
                password        TEXT NOT NULL,
                PRIMARY KEY (empDep, empID)
                );''')

# save changes
con.commit()
print('Employee table created.')

data = [('', '',    'orange colored fruit', 5, 0, 0),
        ('', '',     'sweet substance', 2, 0, 0),
        ('', '',  'powdered almonds', 10, 0, 0),
        ('', '', 'alkalized cocoa powder', 15, 0, 0),
        ('', '',  'ground coffee beans', 1, 0, 0)]

data = [list(row) for row in data]

for row in data:
    uid = authUtils.generateUID()
    cur.execute('select empID from Employee where empID = ?', uid)
    query = cur.fetchone()
    while query is not None:
        uid = authUtils.generateUID()
        cur.execute('select empID from Employee where empID = ?', uid)
        query = cur.fetchone()
    row[1] = uid


# populate table
cur.executemany('insert into AuctionItem values(?,?,?,?,?,?);', data)
con.commit()
print('Data inserted into AuctionItem table.')

# iterate over rows in table
for row in cur.execute('select * from AuctionItem;'):
    print(row)

con.close()
print('Connection closed.')

