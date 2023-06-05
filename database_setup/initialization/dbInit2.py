import random

from utils.databaseUtils import *
from datetime import datetime
import json



with open('complete_db.json') as d:
    data = json.load(d)

special_agents = [e for e in data["employee"] if ((e["firstName"] != 'Prisca') and (e["designation"] == 75))]
project_managers = [e for e in data["employee"] if e["designation"] == 2]
researchers = [e["empID"] for e in data["employee"] if e["designation"] == 79]



def saveData():
    with open("complete_db.json", "w") as output:
        json.dump(data, output, indent=4)

def getAgents(missionStartDate):
    formt = '%Y-%m-%d'
    agents = [a["empID"] for a in special_agents if (datetime.strptime(a["startDate"], formt) <=  datetime.strptime(missionStartDate, formt))]

    print('Mission Start Date: ', missionStartDate)
    print('Agents: ', agents)
    return random.choices(agents, k=random.randint(2, 3))


def originMissionSpecimen():
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
                print('E: ', a, ' M: ', mID)
                manageMission.addEmployeeToMission(a, mID)

            for s in m["specimens"]:
                sID = manageSpecimen.add(s["name"], s["acquisitionDate"], oID, mID, s["threatLevel"], s["notes"],
                                         s["description"])
                s["specimenID"] = sID
                sm = s["medical"]

                spec_researcher = random.choices(researchers, k=random.randint(1, 3))
                s["researchers"] = spec_researcher
                for r in spec_researcher:
                    manageResearcherSpecimen.add(r, sID)

                manageSpecimen.updateSpecimenMedical(sID, sm["bloodtype"], sm["sex"], sm["kilograms"], sm["notes"])
                manageSpecimen.updateSpecimenContainmentStatus(sID, s["statusID"])

originMissionSpecimen()
saveData()
