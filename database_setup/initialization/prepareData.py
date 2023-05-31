import json

with open('base_data.json') as b:
    bData = json.load(b)

with open("ai_data.json") as output:
    aiData = json.load(output)

for e in aiData["employee"]:
    department = None
    for dep in bData["department"]:
        if dep["name"] == e["dep"]:
            department = dep

    if department is None:
        print(e)
        raise ValueError("Department is None!")

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

    print(e["designation"])
    print(e)
    print('\n')


# complete data
with open('complete_data.json', 'w') as c:
    json.dump({"department": bData["department"],
               "employee": bData["employee"] + aiData["employee"],
               "clearanceLevel": aiData["ClearanceLevel"],
               "containmentStatus": aiData["ContainmentStatus"],
               "origin": aiData["origin"]}, c, indent=4)

