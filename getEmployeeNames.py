import sqlite3
from utils.variables import db

con = sqlite3.connect(db)
cur = con.cursor()

cur.execute('SELECT firstName, lastName from Employee')

emps = cur.fetchall()
emps = [list(e) for e in emps]
for e in emps:
    print('{} {}'.format(e[0], e[1]))