import json
import random
from database_setup.declaration.DB_Declaration import *
from datetime import datetime
from utils.encryption import encrypt
from utils.databaseUtils import *

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


depHeads = []


def departmentData():
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
        manageEmployeeDesignation.add(ID, 54)
        manageEmployee.update(ID, endDate=None)
        manageEmployee.updateEmployeeMedical(ID, birth, bt, sex, kg, height, notes)
        manageEmployee.updateEmployeeClearance(ID, 9)
        depHeads.append({
            "dep": depID,
            "designation": 54,
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
            "empID": ID,
            "clearance": 9
        })


def EmployeeData():
    for e in data["commander"]:
        department = None
        for dep in data["department"]:
            if dep["name"] == e["dep"]:
                department = dep


        depID = department["depID"]
        if depID is not None:
            e['dep'] = depID
        else:
            raise ValueError("Department cannot be none!")

        e["sex"] = e["sex"].strip()[0].lower()

        if e["notes"] is not None and e["notes"].lower() == "none":
            e["notes"] = None

        if e["summary"].lower() == "none":
            e["summary"] = None

        for d in department["designations"]:

            if e["designation"] == d[0]:
                e["designation"] = d[2]

    c = data.pop("commander")
    print(c)
    data["employee"] = data["employee"] + c
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
        birth = e["dob"]
        bt = e["bloodtype"]
        sex = e["sex"]
        kg = e["weight"]
        height = e["height"]
        notes = e["notes"]
        e["empID"] = ID = manageEmployee.add(fn, ln, e["dep"], start,
                                             summ)
        manageEmployeeDesignation.add(ID, e["designation"])
        manageEmployee.updateEmployeeMedical(ID, e["dob"], e["bloodtype"], e["sex"], e["weight"], e["height"],
                                             e["notes"])
        e["medical"] = {"dob": birth,
                        "bloodtype": bt,
                        "sex": sex,
                        "weight": kg,
                        "height": height,
                        "notes": notes}

        if "endDate" in e:
            manageEmployee.update(ID, endDate=e["endDate"])
        else:
            e["endDate"] = None

        manageEmployee.updateEmployeeClearance(ID, e["clearance"])

        if e["firstName"] == "Zaria":
            manageEmployee.updateCredentials(ID, encrypt('test'), encrypt('test'))
    data["employee"] = data["employee"] + depHeads





def saveData():
    with open("complete_db.json", "w") as output:
        json.dump(data, output, indent=4)



'''''''''''''''''''''''''''RUN FUNCTIONS'''''''''''''''''''''''''''
designationData()
clearanceData()
containmentStatus()
departmentData()
EmployeeData()

saveData()
