import json
with open('complete_data.json') as d:
    data = json.load(d)



with open('complete_data.json', 'w') as output:
    json.dump(data, output, indent=4)