-- data must first be committed
INSERT INTO employees (employee_id, first_name, last_name, department_id, start_date)
    VALUES ('testing', 'testing', 'testing', 1, CURRENT_DATE);

INSERT INTO specimens (specimen_id, specimen_name, acquisition_date)
    VALUES ('testing', 'testing', CURRENT_DATE);

COMMIT;
BEGIN;
SELECT plan(3);

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


ROLLBACK;


-- test data removal
DELETE FROM employees WHERE first_name = 'testing';
DELETE FROM specimens WHERE specimen_name = 'testing';
SELECT * FROM finish();
COMMIT;