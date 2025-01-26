#!/bin/bash

# Change directory to where the CSV files are located
cd /Users/spicykneecaps/Projects/FSEA/database_setup/csvs || exit

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo ".env file not found! Exiting."
    exit 1
fi

# Step 1: Drop constraints
echo "Dropping foreign key constraints..."
psql "$DB_CONN" -f /Users/spicykneecaps/Projects/FSEA/database_setup/drop_constraints.sql
if [ $? -ne 0 ]; then
    echo "Error occurred while dropping constraints. Exiting."
    exit 1
fi

# Step 2: Truncate tables
echo "Truncating tables..."
psql "$DB_CONN" <<EOF
TRUNCATE TABLE researcher_specimens, employee_missions, department_missions, specimen_medical_records, mission_origins, specimens, missions, employee_medical_records, employee_designations, employee_clearances, employees, origins, designations, departments, containment_statuses, clearances CASCADE;
EOF
if [ $? -ne 0 ]; then
    echo "Error occurred while truncating tables. Exiting."
    exit 1
fi

# Step 3: Load CSV filesb
echo "Loading CSV files..."
psql "$DB_CONN" <<EOF
\copy clearances(clearance_id, clearance_name, description) FROM 'clearances.csv' DELIMITER ',' CSV HEADER;
\copy containment_statuses(containment_status_id, status_name, description) FROM 'containment_statuses.csv' DELIMITER ',' CSV HEADER;
\copy departments(department_id, department_name, director_id, description) FROM 'departments.csv' DELIMITER ',' CSV HEADER;
\copy designations(designation_id, designation_name, abbreviation) FROM 'designations.csv' DELIMITER ',' CSV HEADER;
\copy origins(origin_id, origin_name, discovery_date, description, notes) FROM 'origins.csv' DELIMITER ',' CSV HEADER;
\copy employees(employee_id, department_id, first_name, last_name, start_date, end_date, notes, created, updated) FROM 'employees.csv' DELIMITER ',' CSV HEADER;
\copy employee_clearances(employee_id, clearance_id) FROM 'employee_clearances.csv' DELIMITER ',' CSV HEADER;
\copy employee_designations(employee_id, designation_id) FROM 'employee_designations.csv' DELIMITER ',' CSV HEADER;
\copy employee_medical_records(employee_id, dob, bloodtype, sex, kilograms, height_cm, notes, created, updated) FROM 'employee_medical_records.csv' DELIMITER ',' CSV HEADER;
\copy missions(mission_id, mission_name, start_date, end_date, commander_id, supervisor_id, description, notes) FROM 'missions.csv' DELIMITER ',' CSV HEADER;
\copy specimens(specimen_id, specimen_name, origin_id, mission_id, threat_level, acquisition_date, notes, description) FROM 'specimens.csv' DELIMITER ',' CSV HEADER;
\copy specimen_containment_statuses(specimen_id, containment_status_id) FROM 'specimen_containment_statuses.csv' DELIMITER ',' CSV HEADER;
\copy mission_origins(mission_id, origin_id) FROM 'mission_origins.csv' DELIMITER ',' CSV HEADER;
\copy specimen_medical_records(specimen_id, bloodtype, sex, kilograms, notes) FROM 'specimen_medical_records.csv' DELIMITER ',' CSV HEADER;
\copy department_missions(department_id, mission_id) FROM 'department_missions.csv' DELIMITER ',' CSV HEADER;
\copy employee_missions(employee_id, mission_id, involvement_summary) FROM 'employee_missions.csv' DELIMITER ',' CSV HEADER;
\copy researcher_specimens(employee_id, specimen_id) FROM 'researcher_specimens.csv' DELIMITER ',' CSV HEADER;
\copy resources(resource_id, resource_name, resource_type, description) FROM 'resources.csv' DELIMITER ',' CSV HEADER;
\copy clearance_resource_access(clearance_id, resource_id, access_type) FROM 'clearance_resource_access.csv' DELIMITER ',' CSV HEADER;
EOF
if [ $? -ne 0 ]; then
    echo "Error occurred while loading CSV files. Exiting."
    exit 1
fi

# Step 4: Recreate constraints
echo "Recreating foreign key constraints..."
psql "$DB_CONN" -f /Users/spicykneecaps/Projects/FSEA/database_setup/recreate_constraints.sql
if [ $? -ne 0 ]; then
    echo "Error occurred while recreating constraints. Exiting."
    exit 1
fi

echo "CSV data loaded successfully!"
