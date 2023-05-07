import json
import random

from utils.alterDatabaseUtils import *
from database_setup.DB_Declaration import *

'''
IMPORTANT!!!!
Run DB_Declaration.py EVERYTIME before running this script.
'''

with open('data.json') as d:
    data = json.load(d)
with open('test_data.json') as d:
    test_data = json.load(d)


def departmentData():
    departments = [["Exploration",
                    "The Exploration Department plans and executes missions to explore the universe. They identify "
                    "target destinations, develop new technologies, and coordinate with other departments to ensure "
                    "successful exploration.",
                    [('Mission Planner', 'MP'),
                     ('Project Manager', 'PM'),
                     ('Spacecraft Engineer', 'SE'),
                     ('Flight Director', 'FD'),
                     ('Astrobiologist', 'AB')]],

                   ["Navigation",
                    "The Navigation Department oversees the ship's route planning, ensuring it follows the best "
                    "course to reach destinations identified by the Exploration Department. They maintain the ship's "
                    "navigation systems and map out new routes when necessary.",
                    [('Navigation Officer', 'NO'),
                     ('Route Planner', 'RP'),
                     ('Astronomer', 'AS'),
                     ('Cartographer', 'CA'),
                     ('Geodesist', 'GD')]],

                   ["Science",
                    "The Science Department conducts research on the planets, stars, and other celestial bodies "
                    "encountered during exploration missions. They analyze samples and data and work with other "
                    "departments to ensure that all findings are properly documented.",
                    [('Planetary Scientist', 'PS'),
                     ('Astrophysicist', 'AP'),
                     ('Exobiologist', 'EB'),
                     ('Data Scientist', 'DS'),
                     ('Atmospheric Scientist', 'ASS')
                     ]],

                   ["Engineering",
                    "The Engineering Department designs and builds new technologies and systems to enable "
                    "exploration. They maintain the ship's functionality, improve the ship's overall efficiency, "
                    "conduct repairs, and upgrades as necessary.",
                    [('Chief Engineer', 'CE'),
                     ('Power Systems Engineer', 'PSE'),
                     ('Propulsion Engineer', 'PE'),
                     ('Materials Engineer', 'ME'),
                     ('Systems Engineer', 'SE')
                     ]],

                   ["Communications",
                    "The Communications Department establishes and maintains communication between F-SEA and other "
                    "space-faring organizations. They monitor the ship's internal communication systems and manage "
                    "F-SEA's public relations and media outreach.",
                    [('Communications Officer', 'CO'),
                     ('', ''),
                     ('', ''),
                     ('', ''),
                     ('', '')
                     ]],

                   ["Security",
                    "The Security Department ensures the safety and security of the ship and its crew. They manage "
                    "all security protocols and develop strategies to ensure the crew's safety when exploring "
                    "potentially dangerous environments."],
                   ["Human Resources",
                    "The Human Resources Department manages F-SEA's personnel, including hiring, training, "
                    "and retaining staff. They provide support for crew members' needs, such as healthcare and mental "
                    "health."],
                   ["Supply and Logistics",
                    "The Supply and Logistics Department manages F-SEA's resources, including food, water, fuel, "
                    "and equipment. They ensure that the ship is stocked with everything necessary for successful "
                    "exploration missions and coordinate with other departments to allocate resources properly."],
                   ["Legal",
                    "The Legal Department manages F-SEA's legal affairs. They navigate interstellar laws and "
                    "regulations and ensure that the organization operates within ethical and legal boundaries. They "
                    "draft contracts and agreements with external partners and organizations."],
                   ["Medcial",
                    "This department is responsible for the health and wellbeing of the crew, including providing "
                    "medical care, monitoring crew health, and developing programs to promote overall health and "
                    "wellness."],
                   ["Education",
                    "The Education Department is responsible for providing educational opportunities for crew "
                    "members, including developing curricula, providing access to educational resources, "
                    "and overseeing the ship's library and archives."],
                   ["Cultural Affairs",
                    "The Cultural Affairs Department is responsible for promoting and preserving cultural heritage "
                    "and diversity on the ship. This includes organizing events and celebrations that highlight "
                    "different cultures, providing resources for language and cultural learning, and ensuring that "
                    "cultural artifacts and traditions are properly preserved."],
                   ["Entertainment",
                    "The Entertainment Department is responsible for providing recreational and entertainment "
                    "opportunities for crew members, including organizing social events, managing the ship's "
                    "recreational facilities, and providing access to movies, music, and other forms of "
                    "entertainment."],
                   ["Executive",
                    "The Executive Department oversees the overall strategic direction of the organization, "
                    "manages budgets and resources, and communicates with external stakeholders, such as investors "
                    "and regulatory bodies. This department plays a critical role in ensuring that the organization "
                    "is functioning efficiently and achieving its goals."],
                   ["Special Operations",
                    "The Special Operations Department is responsible for executing critical missions that require "
                    "specialized skills and training, such as rescue operations, high-risk extractions, and covert "
                    "operations. This department works closely with other departments to plan and execute missions "
                    "safely and effectively, while minimizing risk to personnel and equipment."]]

    depInfo = []  # list of dicts, holds depIDs, their names, and their designations for adding employees to appropriate departments later
    for d in departments:
        depInfo.append({"name": d[0], "id": addDepartment(name=d[0], desc=d[1])})
    return depInfo


def employeeData():
    for e in data["employee"]:
        ID = addEmployee(e["firstName"], e["lastName"], e["dep"], e["designation"], e["startDate"], e["summary"])
        updateEmployeeMedical(ID, e["dob"], e["bloodtype"], e["sex"], e["weight"], e["height"], e["notes"])
        if e["firstName"] == "Zaria":
            updateCredentials(ID, 'test', 'test')


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
