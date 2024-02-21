import csv

input_filename = 'missions.csv'
intermediate_filename = 'missionOrigins.csv'
final_filename = 'new_missions.csv'


# Step 3: Create a final CSV with only one of the selected columns
final_columns_to_keep = ['missionID', 'name', 'startDate', 'endDate', 'commanderID', 'supervisorID', 'description']

with open(input_filename, newline='', encoding='utf-8') as infile, \
     open(final_filename, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=final_columns_to_keep)
    writer.writeheader()
    for row in reader:
        writer.writerow({key: row[key] for key in final_columns_to_keep})


