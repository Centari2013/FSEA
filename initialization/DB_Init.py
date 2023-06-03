import json

from utils.databaseUtils import *
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
            manageDesignation.add(des[0], des[1])


def clearanceData():
    for c in data["clearanceLevel"]:
        manageClearance.add(c["name"], c["description"])


def containmentStatus():
    for s in data["containmentStatus"]:
        manageContainmentStatus.add(s["name"], s["description"])


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
        d["depID"] = depID = manageDepartment.add(name=d["name"], desc=d["description"])
        sup = d.pop("supervisor")
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
        d["supervisor"] = ID = manageEmployee.add(fn, ln, depID, start, summary=summ)
        manageDepartment.update(depID, supervisorID=ID)
        manageEmployeeDesignation.add(ID, depSupervisorDesID)
        manageEmployee.update(ID, endDate=None)
        manageEmployee.updateEmployeeMedical(ID, birth, bt, sex, kg, height, notes)

        data["employee"].append({
            "dep": depID,
            "designation": depSupervisorDesID,
            "firstName": fn,
            "lastName": ln,
            "startDate": start,
            "endDate": None,
            "dob": birth,
            "bloodtype": bt,
            "sex": sex,
            "weight": kg,
            "height": height,
            "notes": notes,
            "summary": summ,
            "empID": ID
        })


def EmployeeData():
    for e in data["employee"]:
        for d in data["department"]:
            if d["name"] == e["dep"]:
                e["dep"] = d["depID"]

                for des in d["designations"]:
                    if des[1] == e["designation"]:
                        e["designation"] = des[2]

        fn = e["firstName"]
        ln = e["lastName"]
        start = e["startDate"]
        summ = e["summary"]
        birth = e.pop("dob")
        bt = e.pop("bloodtype")
        sex = e.pop("sex")
        kg = e.pop("weight")
        height = e.pop("height")
        notes = e.pop("notes")
        e["empID"] = ID = manageEmployee.add(fn, ln, e["dep"], start,
                                     summ)
        manageEmployeeDesignation.add(ID, e["designation"])
        manageEmployee.updateEmployeeMedical(ID, e["dob"], e["bloodtype"], e["sex"], e["weight"], e["height"], e["notes"])
        e["medical"] = {"dob": birth,
                        "bloodtype": bt,
                        "sex": sex,
                        "weight": kg,
                        "height": height,
                        "notes": notes}

        if "endDate" in e:
            manageEmployee.update(endDate=e["endDate"])
        else:
            e["endDate"] = None

        manageEmployeeClearance.add(ID, e["clearance"])

        if e["firstName"] == "Zaria":
            manageEmployee.updateCredentials(ID, 'test', 'test')


def originMissionSpecimen():
    for o in data["origin"]:
        oID = manageOrigin.add(o["name"], o["discoveryDate"], o["description"])
        for m in o["missions"]:
            mID = manageMission.add(m["name"], m["description"], oID, m["startDate"], m["endDate"],
                             )


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
