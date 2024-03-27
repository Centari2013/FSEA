
SELECT plan(16);

BEGIN;
-- create clearance
SELECT lives_ok(
    'INSERT INTO clearances (clearance_name, description)
    VALUES (''testing'', ''testing'')',
    'clearances insertion success.'
);

-- create containment_status
SELECT lives_ok (
    'INSERT INTO containment_statuses (status_name, description)
    VALUES (''testing'', ''testing'')',
    'containment_statuses insertion success.'
);

-- create department
SELECT lives_ok (
    'INSERT INTO departments (department_name)
    VALUES (''testing'')',
    'departments insertion success.'
);

-- create designation
SELECT lives_ok (
    'INSERT INTO designations (designation_name, abbreviation)
    VALUES (''testing'', ''test'')',
    'designations insertion success.'
);

-- create employee
SELECT lives_ok(
    'INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES (''testing'', ''testing'', 1, CURRENT_DATE)',
    'employees insertion success.'
    );

-- create employee clearance 
SELECT lives_ok(
    'INSERT INTO employee_clearances (employee_id, clearance_id)
    VALUES (''E7449700'', 1)',
    'employee_clearances insertion success.'
    );

-- create employee designation
SELECT lives_ok(
    'INSERT INTO employee_designations (employee_id, designation_id)
    VALUES (''E7449700'', 1)',
    'employee_designations insertion success.'
);

-- employee_medical_records is automatically inserted into

-- create mission
SELECT lives_ok(
    'INSERT INTO missions (mission_name, description)
    VALUES (''testing'', ''testing'')',
    'missions insertion success.'
    );

-- create origin
SELECT lives_ok(
    'INSERT INTO origins (origin_name, discovery_date, description)
    VALUES (''testing'', CURRENT_DATE, ''testing'')',
    'missions insertion success.'
    );

-- create mission origin
SELECT lives_ok(
    'INSERT INTO mission_origins (mission_id, origin_id)
    VALUES (''M8378606'', ''O2942930'')',
    'mission_origins insertion success.'
    );

-- create specimen
SELECT lives_ok ('INSERT INTO specimens (specimen_name, acquisition_date)
    VALUES (''testing'', CURRENT_DATE)',
    'specimens insertion success.');


-- create specimen containment status
SELECT lives_ok(
    'INSERT INTO specimen_containment_statuses (specimen_id, containment_status_id)
    VALUES (''S3510814'', 1)',
    'specimen_containment_statuses insertion success.'
    );

-- specimen_medical_records is automatically inserted into

-- create specimen mission
SELECT lives_ok(
    'INSERT INTO specimen_missions (specimen_id, mission_id)
    VALUES (''S3510814'', ''M6769658'')',
    'specimen_missions insertion success.'
    );

-- credentials is automatically inserted into 

-- create department mission
SELECT lives_ok(
    'INSERT INTO department_missions (department_id, mission_id)
    VALUES (1, ''M6769658'')',
    'department_missions insertion success.'
    );

-- create employee mission
SELECT lives_ok(
    'INSERT INTO employee_missions (employee_id, mission_id)
    VALUES (''E7449700'', ''M6769658'')',
    'employee_missions insertion success.'
    );


-- create researcher specimen
SELECT lives_ok(
    'INSERT INTO researcher_specimens (employee_id, specimen_id)
    VALUES (''E7449700'', ''S3510814'')',
    'researcher_specimens insertion success.'
    );

SELECT * FROM finish();
ROLLBACK;
