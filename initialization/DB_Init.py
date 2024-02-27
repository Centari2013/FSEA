import json
import random
from datetime import datetime
from old_code.utils.encryption import encrypt
from old_code.utils.databaseUtils import *

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

    for e in data["employee"]:
        fn = e["firstName"]
        ln = e["lastName"]
        start = e["startDate"]
        summ = e["summary"]
        e["empID"] = ID = manageEmployee.add(fn, ln, e["dep"], start,
                                             summ)
        manageEmployeeDesignation.add(ID, e["designation"])
        manageEmployee.updateEmployeeMedical(ID, e["dob"], e["bloodtype"], e["sex"], e["weight"], e["height"],
                                             e["notes"])

        if "endDate" in e:
            manageEmployee.update(ID, endDate=e["endDate"])
        else:
            e["endDate"] = None

        manageEmployee.updateEmployeeClearance(ID, e["clearance"])

        if e["firstName"] == "Zaria":
            manageEmployee.updateCredentials(ID, encrypt('test'), encrypt('test'))
    data["employee"] = data["employee"] + depHeads


def originMissionSpecimen():
    special_agents = [e for e in data["employee"] if ((e["firstName"] != 'Prisca') and (e["designation"] == 75))]
    project_managers = [e for e in data["employee"] if e["designation"] == 2]
    researchers = [e["empID"] for e in data["employee"] if e["designation"] == 79]

    def getAgents(missionStartDate):
        formt = '%Y-%m-%d'
        ag = [age["empID"] for age in special_agents if
                  (datetime.strptime(age["startDate"], formt) <= datetime.strptime(missionStartDate, formt))]
        return list(set(random.choices(ag, k=random.randint(2, 6))))

    for o in data["origin"]:
        oID = manageOrigin.add(o["name"], o["discoveryDate"], o["description"])
        o["originID"] = oID
        for m in o["missions"]:
            agents = getAgents(m["startDate"])
            commander = agents[0]
            supervisor = random.choice(project_managers)["empID"]
            mID = manageMission.add(m["name"], m["description"], m["startDate"], m["endDate"],
                                    commander, supervisor, oID)

            manageDepartment.addMission(o["depID"], mID)

            m["missionID"] = mID
            m["agents"] = agents
            for a in agents:
                manageMission.addEmployeeToMission(a, mID)

            for s in m["specimens"]:
                sID = manageSpecimen.add(s["name"], s["acquisitionDate"], oID, mID, s["threatLevel"], s["notes"],
                                         s["description"])
                s["specimenID"] = sID
                sm = s["medical"]
                print('S: ', sID)
                spec_researcher = list(set(random.choices(researchers, k=random.randint(1, 3))))
                s["researchers"] = spec_researcher
                for r in spec_researcher:
                    manageResearcherSpecimen.add(r, sID)

                manageSpecimen.updateSpecimenMedical(sID, sm["bloodtype"], sm["sex"], sm["kilograms"], sm["notes"])
                manageSpecimen.updateSpecimenContainmentStatus(sID, s["statusID"])


def saveData():
    with open("complete_db.json", "w") as output:
        json.dump(data, output, indent=4)



'''''''''''''''''''''''''''RUN FUNCTIONS'''''''''''''''''''''''''''
designationData()
clearanceData()
containmentStatus()
departmentData()
EmployeeData()
originMissionSpecimen()
saveData()
