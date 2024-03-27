-- All of the following tests are contingent upon the fact that the trigger test have run succesfully.
-- Entity creations will create entries in other tables as specified by their triggers.
-- Entity deletions are supposed to remove those foreign key links.
SELECT plan(3);

-- employee_clearances employee(employee_id) on delete cascade
-- create employee
SELECT lives_ok(
    'INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES (''testing'', ''testing'', 1, CURRENT_DATE)',
    'employees insertion success.'
    );
-- delete employee
SELECT lives_ok(
    'DELETE FROM employees WHERE first_name = ''testing''',
    'employees deletion success.'
);
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM employee_medical_records emr
        JOIN employees e ON emr.employee_id = e.employee_id
        WHERE e.first_name = 'testing'
        ),
        'employees cascade deletion on employee_medical_records success.');



SELECT * FROM finish();