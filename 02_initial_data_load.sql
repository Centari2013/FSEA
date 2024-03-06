-- CSV Uploads via pgAdmin 4
-- Tgis is done before triggers and their functions are implemented so that previous data isn't affected by application logic.
-- The following CSV files were uploaded in the order listed below using the Import/Export tool in pgAdmin 4.
-- This ensures that all foreign key constraints are respected and that the database integrity is maintained.

/*
CSV Upload Order:
1. clearances.csv -> clearances
2. containment_statuses.csv -> containment_statuses
3. departments.csv -> departments
4. designations.csv -> designations
5. department_designations.csv -> department_designations
6. origins.csv -> origins
7. employees.csv -> employees
8. employee_clearances.csv -> employee_clearances
9. employee_designations.csv -> employee_designations
10. employee_medical_records.csv -> employee_medical_records
11. missions.csv -> missions
12. specimens.csv -> specimens
13. mission_origins.csv -> mission_origins
14. specimen_medical_records.csv -> specimen_medical_records
15. department_missions.csv -> department_missions
16. employee_missions.csv -> employee_missions
17. researcher_specimens.csv -> researcher_specimens
*/


-- Note: The actual data import commands are executed within pgAdmin 4 and thus are not represented in this SQL script.
-- This documentation is intended to provide clarity on the data import process for this project.

-- After loading in the data from the csvs, I then ran the following insert statement to keep consistent with the app logic that will be present after implementing triggers.ADD

INSERT INTO credentials (employee_id)
SELECT employee_id 
FROM employees;


-- Employee usernames and passwords will be generated in a later stage of this application's development.
-- I have only deemed this appropriate as this is fictional system that previusly used a rudimentary form of password protection and encryption.
-- Data for the specimen_containment_statuses table will be handles programatically as well.
-- As for the specimen_missions table, that will remain empty until I decide to use it for storytelling purposes.