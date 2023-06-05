import json


with open("complete_data.json") as output:
    data = json.load(output)

data["employee"] = data["employee"] + data["alien"] +

# complete data
with open('complete_data.json', 'w') as c:
    json.dump(data, c, indent=4)

