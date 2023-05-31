import json

from utils.alterDatabaseUtils import *
from database_setup.declaration.DB_Declaration import *

'''
IMPORTANT!!!!
Run DB_Declaration.py EVERYTIME before running this script.
(unless that import statement is still up there)
'''

with open('complete_data.json') as d:
    data = json.load(d)


def designationData():
    for dep in data["department"]:
        for des in dep["designations"]:
            # append designationID to list of designations
            addDesignation(des[0], des[1])


def clearanceData():
    for c in data["clearanceLevel"]:
        addClearance(c["name"], c["description"])


def containmentStatus():
    for s in data["containmentStatus"]:
        addContainmentStatus(s["name"], s["description"])


def departmentData():
    depSupervisorDesID = None
    for dep in data["department"]:
        if dep["name"] == "Executive":
            for des in dep["designations"]:
                if des[1] == "DS":
                    depSupervisorDesID = des[2]
                    break
    # add generated depID to each department dict
    for d in data["department"]:
        d["depID"] = depID = addDepartment(name=d["name"], desc=d["description"])
        sup = d["supervisor"]
        fn = sup["firstName"]
        ln = sup["lastName"]
        start = sup["startDate"]
        summ = sup["summary"]
        birth = sup["dob"]
        bt = sup["bloodtype"]
        sex = sup["sex"]
        kg = sup["weight"]
        height = sup["height"]
        notes = sup["notes"]
        # add department supervisors
        d["supervisor"] = ID = addEmployee(fn, ln, depID, start, summary=summ)
        updateDepartment(depID, supervisorID=ID)
        addEmployeeDesignation(ID, depSupervisorDesID)
        updateEmployee(ID, endDate=None)
        updateEmployeeMedical(ID, birth, bt, sex, kg, height, notes)


def EmployeeData():
    for e in data["employee"]:
        for d in data["department"]:
            if d["name"] == e["dep"]:
                e["dep"] = d["depID"]

                for des in d["designations"]:
                    if des[1] == e["designation"]:
                        e["designation"] = des[2]

        e["empID"] = ID = addEmployee(e["firstName"], e["lastName"], e["dep"], e["startDate"],
                                      e["summary"])
        addEmployeeDesignation(ID, e["designation"])
        updateEmployeeMedical(ID, e["dob"], e["bloodtype"], e["sex"], e["weight"], e["height"], e["notes"])

        if "endDate" in e:
            updateEmployee(endDate=e["endDate"])

        addEmployeeClearance(ID, e["clearance"])

        if e["firstName"] == "Zaria":
            updateCredentials(ID, 'test', 'test')


def saveData():
    with open("complete_db.json", "w") as output:
        json.dump(data, output, indent=4)


'''''''''''''''''''''''''''PRINT TABLES'''''''''''''''''''''''''''


def printTables():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    print('Department Table')
    for row in cur.execute('SELECT * FROM Department;'):
        print(row)
    print('\n')

    print('Designation Table')
    for row in cur.execute('SELECT * FROM Designation;'):
        print(row)
    print('\n')

    print('EmployeeDesignation Table')
    for row in cur.execute('SELECT * FROM EmployeeDesignation;'):
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
