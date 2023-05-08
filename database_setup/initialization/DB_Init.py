import json
import random
import names

from utils.alterDatabaseUtils import *
from database_setup.declaration.DB_Declaration import *

'''
IMPORTANT!!!!
Run DB_Declaration.py EVERYTIME before running this script.
'''

with open('data.json') as d:
    data = json.load(d)
with open('test_data.json') as d:
    test_data = json.load(d)


def departmentData():
    # list of dicts, holds depIDs, their names, and their designations for adding employees to appropriate departments later
    for d in data["department"]:
        d["depID"] = addDepartment(name=d["name"], desc=d["description"])



def employeeData():
    for e in data["employee"]:
        for d in data["department"]:
            if d["name"] == e["dep"]:
                e["dep"] = d["depID"]

        e["empID"] = ID = addEmployee(e["firstName"], e["lastName"], e["dep"], e["designation"], e["startDate"], e["summary"])
        updateEmployeeMedical(ID, e["dob"], e["bloodtype"], e["sex"], e["weight"], e["height"], e["notes"])
        if e["firstName"] == "Zaria":
            updateCredentials(ID, 'test', 'test')

    for d in data["department"]:
        executiveDepID = d.get("depID")
        # TODO get designation IDs
        if d["name"] != "Exploration":
            fn = names.get_first_name()
            ln = names.get_last_name()
            d["supervisor"] = addEmployee(fn, ln, executiveDepID, )



originIDs = []


def originData():
    for o in data["origin"]:
        originIDs.append(addOrigin(o["name"], o["description"]))

    for o in test_data["origin"]:
        originIDs.append(addOrigin(o["name"], o["description"]))


missionIDs = []


def missionData():
    for m in data["mission"]:
        missionIDs.append(addMission(m["name"], m["description"]))
    for m in test_data["mission"]:
        missionIDs.append(addMission(m["name"], m["description"]))


def originMissionLink():
    for oid in originIDs:
        updateOrigin(oid, missionID=random.choice(missionIDs))

    for mid in missionIDs:
        updateMission(mid, originID=random.choice(originIDs))


def specimenData():
    for s in data["specimen"]:
        addSpecimen(name=s['name'], acquisitionDate=s["acquisitionDate"], notes=s["notes"])

    for s in test_data["specimen"]:
        addSpecimen(name=s['name'], acquisitionDate=s["acquisitionDate"], notes=s["notes"])


departmentData()
employeeData()

originData()
missionData()
originMissionLink()

specimenData()


with open("complete_data.json", "w") as output:
    json.dump(data, output)

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# add test user
"""cur.execute('''UPDATE Credentials
                SET username = ?, password = ?
                WHERE empID = (SELECT empID
                                FROM Employee
                                WHERE firstName = 'Zaria');''', (encrypt('test'), encrypt('test')))
con.commit()"""

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
