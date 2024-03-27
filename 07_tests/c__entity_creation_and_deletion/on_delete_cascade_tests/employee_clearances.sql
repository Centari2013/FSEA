-- All of the following tests are contingent upon the fact that the trigger test have run successfully.
-- Employee and Clearance creations will create entries in the employee_clearances table as specified by their triggers.
-- Employee and Clearances deletions are supposed to remove those foreign key links from the employee_clearances table.
SELECT plan(10);

-- employee_clearances employee(employee_id) on delete cascade
-- create employee
SELECT lives_ok(
    'INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES (''testing'', ''testing'', 1, CURRENT_DATE)',
    'employees insertion success.'
    );
-- insert into employee_clearances
SELECT lives_ok(
    'INSERT INTO employee_clearances (employee_id, clearance_id)
    SELECT e.employee_id, c.clearance_id
    FROM employees e, clearances c
    WHERE e.first_name = ''testing'' AND c.clearance_name = ''testing''',
    'employee_clearances insertion success.'
    );

-- delete employee
SELECT lives_ok(
    'DELETE FROM employees WHERE first_name = ''testing''',
    'employees deletion success.'
);
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM employee_clearances ec
        JOIN employees e ON ec.employee_id = e.employee_id
        WHERE e.first_name = 'testing'
        ),
        'employees cascade deletion on employee_clearances success.');
-- cleanup clearance
SELECT lives_ok(
    'DELETE FROM clearances WHERE clearance_name = ''testing''',
    'clearances cleanup success.'
);



-- employee_clearances clearances(clearance_id) on delete cascade
-- create employee
SELECT lives_ok(
    'INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES (''testing'', ''testing'', 1, CURRENT_DATE)',
    'employees insertion success.'
    );
-- insert into employee_clearances
SELECT lives_ok(
    'INSERT INTO employee_clearances (employee_id, clearance_id)
    SELECT e.employee_id, c.clearance_id
    FROM employees e, clearances c
    WHERE e.first_name = ''testing'' AND c.clearance_name = ''testing''',
    'employee_clearances insertion success.'
    );


-- delete clearance
SELECT lives_ok(
    'DELETE FROM clearances WHERE clearance_name = ''testing''',
    'clearances deletion success.'
);
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM employee_clearances ec
        JOIN clearances c ON ec.clearance_id = c.clearance_id
        WHERE c.clearance_name = 'testing'
        ),
        'clearances cascade deletion on employee_clearances success.');

-- cleanup employee
SELECT lives_ok(
    'DELETE FROM employees WHERE first_name = ''testing''',
    'employees cleanup success.'
);
SELECT * FROM finish();