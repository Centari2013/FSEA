
SELECT plan(30);

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



-- test data cleanup
-- cleanup researcher_specimens
SELECT lives_ok(
    'DELETE FROM researcher_specimens WHERE employee_id = ''E7449700'' AND specimen_id = ''S3510814''',
    'researcher_specimens cleanup success.'
);

-- cleanup employee_missions
SELECT lives_ok(
    'DELETE FROM employee_missions WHERE employee_id = ''E7449700'' AND mission_id = ''M6769658''',
    'employee_missions cleanup success.'
);

-- cleanup department_missions
SELECT lives_ok(
    'DELETE FROM department_missions WHERE department_id = 1 AND mission_id = ''M6769658''',
    'department_missions cleanup success.'
);

-- cleanup specimen_missions
SELECT lives_ok(
    'DELETE FROM specimen_missions WHERE specimen_id = ''S3510814'' AND mission_id = ''M6769658''',
    'specimen_missions cleanup success.'
);

-- cleanup specimen_containment_statuses
SELECT lives_ok(
    'DELETE FROM specimen_containment_statuses WHERE specimen_id = ''S3510814''',
    'specimen_containment_statuses cleanup success.'
);

-- cleanup specimens
SELECT lives_ok(
    'DELETE FROM specimens WHERE specimen_name = ''testing''',
    'specimens cleanup success.'
);

-- cleanup origins
SELECT lives_ok(
    'DELETE FROM origins WHERE origin_name = ''testing''',
    'origins cleanup success.'
);

-- cleanup missions
SELECT lives_ok(
    'DELETE FROM missions WHERE mission_name = ''testing''',
    'missions cleanup success.'
);

-- cleanup employee_designations
SELECT lives_ok(
    'DELETE FROM employee_designations WHERE employee_id = ''E7449700''',
    'employee_designations cleanup success.'
);

-- cleanup employee_clearances
SELECT lives_ok(
    'DELETE FROM employee_clearances WHERE employee_id = ''E7449700''',
    'employee_clearances cleanup success.'
);

-- cleanup employees
SELECT lives_ok(
    'DELETE FROM employees WHERE first_name = ''testing'' AND last_name = ''testing''',
    'employees cleanup success.'
);

-- cleanup designations
SELECT lives_ok(
    'DELETE FROM designations WHERE designation_name = ''testing''',
    'designations cleanup success.'
);

-- cleanup departments
SELECT lives_ok(
    'DELETE FROM departments WHERE department_name = ''testing''',
    'departments cleanup success.'
);

-- cleanup containment_statuses
SELECT lives_ok (
    'DELETE FROM containment_statuses WHERE status_name = ''testing''',
    'containment_statuses cleanup success.'
);

-- cleanup clearances
SELECT lives_ok(
    'DELETE FROM clearances WHERE clearance_name = ''testing''',
    'clearances cleanup success.'
);


SELECT * FROM finish();

