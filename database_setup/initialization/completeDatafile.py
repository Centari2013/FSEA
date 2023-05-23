import json

with open('ai_data.json') as a:
    aiData = json.load(a)

with open('base_data.json') as b:
    bData = json.load(b)

with open('complete_data.json', 'w') as c:
    json.dump({"department": bData["department"],
               "employee": bData["employee"] + aiData["employee"]}, c, indent=4)