import random
import json
import names
from essential_generators import DocumentGenerator
from utils.dbVariables import *

gen = DocumentGenerator()


for d in departments:
    data["department"].append({"name": d[0],
                               "description": d[1]})

for i in range(1000):
    data["employee"].append({
        "dep": random.randrange(1, numOfDepartments + 1),
        "designation": random.choice(designation),
        "firstName": names.get_first_name(),
        "lastName": names.get_last_name(),
        "startDate": "2023-09-22",
        "dob": "2000-09-22",
        "bloodtype": random.choice(bloodtypes),
        "sex": random.choice(sex),
        "weight": round(random.uniform(55, 85), 1),
        "height": round(random.uniform(120, 180), 1),
        "notes": None,
        "summary": gen.paragraph()
    })

for i in range(250):
    data["origin"].append({
        "name": "origin" + str(i),
        "description": gen.paragraph()
    })

for i in range(3000):
    data["mission"].append({
        "name": "mission" + str(i),
        "description": gen.paragraph()
    })

for i in range(300):
    data["specimen"].append({
        "name": "specimen" + str(i),
        "acquisitionDate": "0000-00-00",
        "notes": gen.paragraph(),
        "summary": gen.paragraph()
    })

with open('../initialization/test_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)
