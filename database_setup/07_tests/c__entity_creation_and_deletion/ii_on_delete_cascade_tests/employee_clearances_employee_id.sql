
-- create test data
CREATE TEMP TABLE test_ids (
    id SERIAL,
    e_id VARCHAR(8),
    c_id INTEGER
);

DO $$
DECLARE
    v_employee_id VARCHAR(8);
    v_clearance_id INTEGER;
BEGIN
  
    INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES ('testing', 'testing', 1, CURRENT_DATE)
    RETURNING employee_id INTO v_employee_id;
  
  
    INSERT INTO test_ids (e_id)
    VALUES (v_employee_id);

    INSERT INTO clearances (clearance_name, description)
    VALUES ('testing', 'testing')
    RETURNING clearance_id INTO v_clearance_id;

    UPDATE test_ids
    SET c_id = v_clearance_id
    WHERE id = 1;

    INSERT INTO employee_clearances (employee_id, clearance_id)
    SELECT e_id, c_id
    FROM test_ids
    WHERE id = 1;

END;
$$;

-- delete employee
DELETE FROM employees e
WHERE e.employee_id = (SELECT e_id FROM test_ids);

SELECT plan(1);

-- employee_clearances employee(employee_id) on delete cascade

SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM employee_clearances
        WHERE employee_id = (SELECT e_id FROM test_ids)
        ),
        'employees cascade deletion on employee_clearances success.');

-- cleanup clearance
DELETE FROM clearances WHERE clearance_id = (SELECT c_id FROM test_ids);




SELECT * FROM finish();