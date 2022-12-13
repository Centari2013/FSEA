import json

with open('utils/data.json') as d:
    data = json.load(d)

for e in data["employee"]:
    print('{} {}'.format(e["firstName"], e["lastName"]))

