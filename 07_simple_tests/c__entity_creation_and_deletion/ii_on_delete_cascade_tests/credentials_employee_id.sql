BEGIN;

-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(8)
);

DO $$
DECLARE
    v_employee_id VARCHAR(8);
BEGIN
    -- Insert a test employee
    INSERT INTO employees (employee_id, first_name, last_name, department_id, start_date)
    VALUES ('testing', 'Test', 'Employee', 1, CURRENT_DATE)
    RETURNING employee_id INTO v_employee_id;

    -- Capture test ID
    INSERT INTO test_ids (employee_id)
    VALUES (v_employee_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on employee_id
DELETE FROM employees WHERE employee_id = (SELECT employee_id FROM test_ids);

-- Verify cascading deletion in credentials
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM credentials
        WHERE employee_id = (SELECT employee_id FROM test_ids)
    ),
    'Deleting an employee cascades deletion to credentials'
);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
