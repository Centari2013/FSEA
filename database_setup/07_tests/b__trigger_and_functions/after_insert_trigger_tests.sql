BEGIN;
-- insert test data
CREATE TEMP TABLE test_ids (
    id SERIAL,
    e_id VARCHAR(8),
    s_id VARCHAR(8)
);

DO $$
DECLARE
    v_employee_id VARCHAR(8);
    v_specimen_id VARCHAR(8);
BEGIN
  
    INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES ('testing', 'testing', 1, CURRENT_DATE)
    RETURNING employee_id INTO v_employee_id;
  
  
    INSERT INTO test_ids (e_id)
    VALUES (v_employee_id);

    INSERT INTO specimens (specimen_name, acquisition_date)
    VALUES ('testing', CURRENT_DATE)
    RETURNING specimen_id INTO v_specimen_id;

    UPDATE test_ids
    SET s_id = v_specimen_id
    WHERE id = 1;

END;
$$;


SELECT plan(3);


-- the following tests are structured as such due to auto-generated ids
-- create_employee_records 
-- part 1: check insert on employee_medical_records

SELECT is(
    CAST ((
        SELECT COUNT(*) 
        FROM employees e
        JOIN employee_medical_records emr ON e.employee_id = emr.employee_id
        WHERE e.employee_id = (SELECT e_id FROM test_ids)
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
        WHERE e.employee_id = (SELECT e_id FROM test_ids)
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
        WHERE s.specimen_id = (SELECT s_id FROM test_ids)
    ) AS integer),
    1,
    'create_specimen_medical_record trigger correctly inserts into specimen_medical_records'
);

SELECT * FROM finish();


-- test data removal
DELETE FROM employees WHERE employee_id = (SELECT e_id FROM test_ids);
DELETE FROM specimens WHERE specimen_id = (SELECT s_id FROM test_ids);

ROLLBACK;