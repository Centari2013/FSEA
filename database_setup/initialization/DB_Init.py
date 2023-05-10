import json
import random
import names
import numpy.random
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

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


def generateDateList(startDate, endDate):
    generatedDates = [startDate]

    # loop to get each date till end date
    while startDate != endDate:
        startDate += timedelta(days=1)
        generatedDates.append(startDate)

    return generatedDates


birthdate_ranges = [generateDateList(date(1995, 1, 1), date(2020, 1, 1)),
                    generateDateList(date(2021, 1, 1), date(2045, 1, 1)),
                    generateDateList(date(2046, 1, 1), date(2057, 1, 1))]


def getRandomBSEDates():
    current_year = 2075

    chosen_range_list = birthdate_ranges[numpy.random.choice(numpy.arange(3), p=[0.1, 0.4, 0.5])]

    birthDate = random.choice(chosen_range_list)
    hire_age = random.randint(18, 35)
    days_to_add = random.randint(180)

    startDate = birthDate + relativedelta(years=hire_age, days=days_to_add)

    endDate = None

    if current_year - birthDate.year > 65:
        endDate = birthDate + relativedelta(years=65, days=random.randint(30))

    birthDate = birthDate.strftime("%Y-%m-%d")
    startDate = startDate.strftime("%Y-%m-%d")
    endDate = endDate.strftime("%Y-%m-%d")

    return birthDate, startDate, endDate


def departmentData():
    # add generated depID to each department dict
    for d in data["department"]:
        d["depID"] = addDepartment(name=d["name"], desc=d["description"])


def designationData():
    with data["department"]["designations"] as des:
        for d in des:
            # append designationID to list of designations
            d.append(addDesignation(d[0], d[1]))


# TODO: feed list of possible designations to ChatGPT and ask it to generate a JSON of 100 employess with relevant
#  attributes
def employeeData():
    for e in data["employee"]:
        for d in data["department"]:
            if d["name"] == e["dep"]:
                e["dep"] = d["depID"]

                for des in d["designations"]:
                    if des[1] == e["designation"]:
                        e["designation"] = des[2]

        e["empID"] = ID = addEmployee(e["firstName"], e["lastName"], e["dep"], e["designation"], e["startDate"],
                                      e["summary"])
        updateEmployeeMedical(ID, e["dob"], e["bloodtype"], e["sex"], e["weight"], e["height"], e["notes"])

        if e["firstName"] == "Zaria":
            updateCredentials(ID, 'test', 'test')

    # add department supervisors
    executiveDepID = None
    depSupervisorDesID = None
    for dep in data["department"]:
        if dep["name"] == "Executive":
            executiveDepID = dep["depID"]
            for des in dep["designations"]:
                if des[1] == "DS":
                    depSupervisorDesID = des[2]
                    break

    for d in data["department"]:

        # The Exploration department already has a supervisor in data.json
        if d["name"] != "Exploration":
            fn = names.get_first_name()
            ln = names.get_last_name()
            birth, start, end = getRandomBSEDates()
            d["supervisor"] = ID = addEmployee(fn, ln, executiveDepID, depSupervisorDesID, start, summary=None)
            updateEmployee(ID, endDate=end)
            updateEmployeeMedical(ID, birth)


departmentData()
employeeData()

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
