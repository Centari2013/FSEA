#!/bin/bash

# Change directory to where the CSV files are located
cd /home/centari/Desktop/Projects/FSEA/database_setup/csvs

# Connect to the PostgreSQL database and run the following commands

psql -d fsea -U postgres <<EOF

-- Disable foreign key constraint checks
SET session_replication_role = replica;

-- Truncate tables, starting with those that have dependencies
TRUNCATE TABLE researcher_specimens, employee_missions, department_missions, specimen_medical_records, mission_origins, specimens, missions, employee_medical_records, employee_designations, employee_clearances, employees, origins, designations, departments, containment_statuses, clearances CASCADE;

-- Re-enable foreign key constraint checks
SET session_replication_role = DEFAULT;


-- clearances.csv -> clearances
\copy clearances(clearance_id, clearance_name, description) FROM 'clearances.csv' DELIMITER ',' CSV HEADER;

-- containment_statuses.csv -> containment_statuses
\copy containment_statuses(containment_status_id, status_name, description) FROM 'containment_statuses.csv' DELIMITER ',' CSV HEADER;

-- departments.csv -> departments
\copy departments(department_id, department_name, director_id, description) FROM 'departments.csv' DELIMITER ',' CSV HEADER;

-- designations.csv -> designations
\copy designations(designation_id, designation_name, abbreviation) FROM 'designations.csv' DELIMITER ',' CSV HEADER;

-- origins.csv -> origins
\copy origins(origin_id, origin_name, discovery_date, description, notes) FROM 'origins.csv' DELIMITER ',' CSV HEADER;

-- employees.csv -> employees
\copy employees(employee_id, department_id, first_name, last_name, start_date, end_date, notes, created, updated) FROM 'employees.csv' DELIMITER ',' CSV HEADER;

-- employee_clearances.csv -> employee_clearances
\copy employee_clearances(employee_id, clearance_id) FROM 'employee_clearances.csv' DELIMITER ',' CSV HEADER;

-- employee_designations.csv -> employee_designations
\copy employee_designations(employee_id, designation_id) FROM 'employee_designations.csv' DELIMITER ',' CSV HEADER;

-- employee_medical_records.csv -> employee_medical_records
\copy employee_medical_records(employee_id, dob, bloodtype, sex, kilograms, height_cm, notes, created, updated) FROM 'employee_medical_records.csv' DELIMITER ',' CSV HEADER;

-- missions.csv -> missions
\copy missions(mission_id, mission_name, start_date, end_date, commander_id, supervisor_id, description, notes) FROM 'missions.csv' DELIMITER ',' CSV HEADER;

-- specimens.csv -> specimens
\copy specimens(specimen_id, specimen_name, origin_id, mission_id, threat_level, acquisition_date, notes, description) FROM 'specimens.csv' DELIMITER ',' CSV HEADER;

-- specimen_containment_statuses.csv -> specimen_containment_statuses
\copy specimen_containment_statuses(specimen_id, containment_status_id) FROM 'specimen_containment_statuses.csv' DELIMITER ',' CSV HEADER;

-- mission_origins.csv -> mission_origins
\copy mission_origins(mission_id, origin_id) FROM 'mission_origins.csv' DELIMITER ',' CSV HEADER;

-- specimen_medical_records.csv -> specimen_medical_records
\copy specimen_medical_records(specimen_id, bloodtype, sex, kilograms, notes) FROM 'specimen_medical_records.csv' DELIMITER ',' CSV HEADER;

-- department_missions.csv -> department_missions
\copy department_missions(department_id, mission_id) FROM 'department_missions.csv' DELIMITER ',' CSV HEADER;

-- employee_missions.csv -> employee_missions
\copy employee_missions(employee_id, mission_id, involvement_summary) FROM 'employee_missions.csv' DELIMITER ',' CSV HEADER;

-- researcher_specimens.csv -> researcher_specimens
\copy researcher_specimens(employee_id, specimen_id) FROM 'researcher_specimens.csv' DELIMITER ',' CSV HEADER;

-- resources.csv -> resources
\copy resources(resource_id, resource_name) FROM 'researcher_specimens.csv' DELIMITER ',' CSV HEADER;

-- clearance_resource_access.csv -> clearance_resource_access
\copy clearance_resource_access(clearance_id, resource_id, access_type) FROM 'clearance_resource_access.csv' DELIMITER ',' CSV HEADER;

EOF
