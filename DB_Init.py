import sqlite3
from utils.variables import db
from utils.databaseUtils import *
import json

with open('utils/data.json') as d:
    data = json.load(d)

for d in data["department"]:
    addDepartment(d['name'], desc=d['description'])

for e in data["employee"]:
    print(e)
    ID = addEmployee(e['firstName'], e['lastName'], e['dep'], e['designation'], e['startDate'])


con = sqlite3.connect(db)
cur = con.cursor()
# iterate over rows in table
print('Department Table')
for row in cur.execute('SELECT * FROM Department;'):
    print(row)
print('\n')


print('Employee Table')
for row in cur.execute('SELECT * FROM Employee;'):
    print(row)
print('\n')
'''
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
'''
