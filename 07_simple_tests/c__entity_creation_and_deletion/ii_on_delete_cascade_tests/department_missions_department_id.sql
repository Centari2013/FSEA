BEGIN;

-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL PRIMARY KEY,
    department_id INTEGER,
    mission_id VARCHAR(8)
);

DO $$
DECLARE
    v_department_id INTEGER;
    v_mission_id VARCHAR(8);
BEGIN
    -- Insert a test department
    INSERT INTO departments (department_name, description)
    VALUES ('testing', 'testing')
    RETURNING department_id INTO v_department_id;
  
    -- Insert a test mission
    INSERT INTO missions (mission_id, mission_name, description)
    VALUES ('testing', 'testing', 'testing')
    RETURNING mission_id INTO v_mission_id;

    -- Associate department and mission
    INSERT INTO department_missions (department_id, mission_id)
    VALUES (v_department_id, v_mission_id);

    -- Capture test IDs
    INSERT INTO test_ids (department_id, mission_id)
    VALUES (v_department_id, v_mission_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on department_id
DELETE FROM departments WHERE department_id = (SELECT department_id FROM test_ids);

-- Verify cascading deletion in department_missions
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM department_missions
        WHERE department_id = (SELECT department_id FROM test_ids)
    ),
    'Deleting a department cascades deletion to department_missions'
);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
