import json

with open('department_data.json') as d:
    depData = json.load(d)

with open("ai_data.json") as output:
    aiData = json.load(output)["employee"]


for e in aiData:
    department = None
    for dep in depData["department"]:
        if dep["name"] == e["dep"]:
            department = dep


    if department is None:
        print(e)
        raise ValueError("Department is None!")

    #print(department)
    depID = department["id"]
    if depID is not None:
        e['dep'] = depID
    else:
        raise ValueError("Department cannot be none!")

    e["sex"] = e["sex"].strip()[0].lower()

    if e["notes"] is not None and e["notes"].lower() == "none":
        e["notes"] = None

    if e["summary"].lower() == "none":
        e["summary"] = None

    print(e["designation"])
    print(e)
    print('\n')
    for d in department["designations"]:

        if e["designation"] == d[0]:
            e["designation"] = d[2]
        

    print(e["designation"])
    print(e)
    print('\n')


empData = {"employee": aiData}
with open("clean_ai_data.json", "w") as output:
    json.dump(empData, output, indent=4)