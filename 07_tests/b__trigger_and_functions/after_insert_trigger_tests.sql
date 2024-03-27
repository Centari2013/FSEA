SELECT plan(7);

-- data must first be committed
SELECT lives_ok(
    'INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES (''testing'', ''testing'', 1, CURRENT_DATE)',
    'Insert of test employee successful.'
    );

SELECT lives_ok ('INSERT INTO specimens (specimen_name, acquisition_date)
    VALUES (''testing'', CURRENT_DATE)',
    'Insert of test specimen successful.');



-- the following tests are structured as such due to auto-generated ids
-- create_employee_records 
-- part 1: check insert on employee_medical_records

SELECT is(
    CAST ((
        SELECT COUNT(*) 
        FROM employees e
        JOIN employee_medical_records emr ON e.employee_id = emr.employee_id
        WHERE e.first_name = 'testing'
    ) AS integer),
    1,
    'create_employee_records trigger correctly inserts into employee_medical_records'
);
-- part 2: check insert on credentials
SELECT is(
    CAST((
        SELECT COUNT(*) 
        FROM employees e
        JOIN credentials c ON e.employee_id = c.employee_id
        WHERE e.first_name = 'testing'
    ) AS integer),
    1,
    'create_employee_records trigger correctly inserts into credentials'
);

-- create_specimen_medical_record
SELECT is(
    CAST((
        SELECT COUNT(*) 
        FROM specimens s
        JOIN specimen_medical_records smr ON s.specimen_id = smr.specimen_id
        WHERE s.specimen_name = 'testing'
    ) AS integer),
    1,
    'create_specimen_medical_record trigger correctly inserts into specimen_medical_records'
);



-- test data removal
SELECT lives_ok (
    'DELETE FROM employees WHERE first_name = ''testing''',
    'Deletion of test employee successful.');
SELECT lives_ok (
    'DELETE FROM specimens WHERE specimen_name = ''testing''',
    'Deletion of test specimen successful.');
SELECT * FROM finish();
