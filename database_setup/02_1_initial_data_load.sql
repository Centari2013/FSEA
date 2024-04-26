-- CSV Uploads via pgAdmin 4
-- This is done before triggers and their functions are implemented so that previous data isn't affected by application logic.
-- The following CSV files were uploaded in the order listed below using the Import/Export tool in pgAdmin 4.
-- This ensures that all foreign key constraints are respected and that the database integrity is maintained.

/*
CSV Upload Order:
1. clearances.csv -> clearances
2. containment_statuses.csv -> containment_statuses
3. departments.csv -> departments
4. designations.csv -> designations
5. origins.csv -> origins
6. employees.csv -> employees
7. employee_clearances.csv -> employee_clearances
8. employee_designations.csv -> employee_designations
9. employee_medical_records.csv -> employee_medical_records
10. missions.csv -> missions
11. specimens.csv -> specimens
12. specimen_containment_statuses -> specimen_containment_statuses
13. mission_origins.csv -> mission_origins
14. specimen_medical_records.csv -> specimen_medical_records
15. department_missions.csv -> department_missions
16. employee_missions.csv -> employee_missions
17. researcher_specimens.csv -> researcher_specimens
18. resources.csv -> resources
19. clearance_resource_access.csv -> clearance_resource_access
*/


-- Note: The actual data import commands are executed using a bash script which can be found in this same directory.

-- After loading in the data from the csvs, I then ran the following insert statement to keep consistent with the app logic that will be present after implementing triggers.ADD

INSERT INTO credentials (employee_id)
SELECT employee_id 
FROM employees;


-- And this statement is to ensure that only valid employees can become directors of departments.
ALTER TABLE departments 
ADD CONSTRAINT fk_director_id 
FOREIGN KEY (director_id) 
REFERENCES employees(employee_id)
;

-- Employee usernames and passwords will be generated in a later stage of this application's development.
-- I have only deemed this appropriate as this is fictional system that previusly used a rudimentary form of password protection and encryption.
-- Data for the specimen_containment_statuses table will be handled programatically as well.
-- As for the specimen_missions table, that will remain empty until I decide to use it for storytelling purposes.

-- And now we have to fix the serial counters for the tables that use them

-- Adjust sequence for clearances
SELECT setval('clearances_clearance_id_seq', (SELECT MAX(clearance_id) FROM clearances) + 1, false);
-- Adjust sequence for containment_statuses
SELECT setval('containment_statuses_containment_status_id_seq', (SELECT MAX(containment_status_id) FROM containment_statuses) + 1, false);

-- Adjust sequence for departments
SELECT setval('departments_department_id_seq', (SELECT MAX(department_id) FROM departments) + 1, false);

-- Adjust sequence for designations
SELECT setval('designations_designation_id_seq', (SELECT MAX(designation_id) FROM designations) + 1, false);
