import json

from DB_Declaration import *
from utils.alterDatabaseUtils import *

'''
IMPORTANT!!!!
Run DB_Declaration.py EVERYTIME before running this script.
'''

with open('utils/test_data.json') as d:
    data = json.load(d)


def departmentData():
    for d in data["department"]:
        addDepartment(name=d["name"], desc=d["description"])


def employeeData():
    for e in data["employee"]:
        ID = addEmployee(e["firstName"], e["lastName"], e["dep"], e["designation"], e["startDate"], e["summary"])
        updateEmployeeMedical(ID, e["dob"], e["bloodtype"], e["sex"], e["weight"], e["height"], e["notes"])


def originData():
    for o in data["origin"]:
        oID = addOrigin(o["name"], o["description"])


def missionData():
    for m in data["mission"]:
        mID = addMission(m["name"], m["description"])


def specimenData():
    for s in data["specimen"]:
        addSpecimen(s['name'], s["acquisitionDate"], notes=s["notes"], )


departmentData()

con = sqlite3.connect(db)
cur = con.cursor()

# add test user
cur.execute('''UPDATE Credentials
                SET username = ?, password = ?
                WHERE empID = (SELECT empID
                                FROM Employee
                                WHERE firstName = 'Zaria');''', (encrypt('test'), encrypt('test')))
con.commit()

'''''''''''''''''''''''''''PRINT TABLES'''''''''''''''''''''''''''
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
    row[1] = decrypt(row[1])
    row[2] = decrypt(row[2])
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

print('Specimen Table')
for row in cur.execute('SELECT * FROM Specimen;'):
    row = list(row)
    print(row)
print('\n')

print('SpecimenMedical Table')
for row in cur.execute('SELECT * FROM SpecimenMedical;'):
    row = list(row)
    print(row)
print('\n')

con.close()
print('Database connection closed.')
