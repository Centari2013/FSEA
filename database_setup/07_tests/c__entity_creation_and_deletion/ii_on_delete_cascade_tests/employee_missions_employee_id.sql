BEGIN;

-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(8),
    mission_id VARCHAR(8)
);

DO $$
DECLARE
    v_employee_id VARCHAR(8);
    v_mission_id VARCHAR(8);
BEGIN
    -- Insert a test employee
    INSERT INTO employees (employee_id, first_name, last_name, department_id, start_date)
    VALUES ('testing', 'testing', 'testing', 1, CURRENT_DATE)
    RETURNING employee_id INTO v_employee_id;
  
    -- Insert a test mission
    INSERT INTO missions (mission_id, mission_name, description)
    VALUES ('testing', 'testing', 'testing')
    RETURNING mission_id INTO v_mission_id;

    -- Associate employee and mission
    INSERT INTO employee_missions (employee_id, mission_id, involvement_summary)
    VALUES (v_employee_id, v_mission_id, 'testing');

    -- Capture test IDs
    INSERT INTO test_ids (employee_id, mission_id)
    VALUES (v_employee_id, v_mission_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on employee_id
DELETE FROM employees WHERE employee_id = (SELECT employee_id FROM test_ids);

-- Verify cascading deletion in employee_missions
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM employee_missions
        WHERE employee_id = (SELECT employee_id FROM test_ids)
    ),
    'Deleting an employee cascades deletion to employee_missions'
);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
