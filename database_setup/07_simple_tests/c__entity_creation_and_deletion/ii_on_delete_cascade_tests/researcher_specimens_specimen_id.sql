BEGIN;

-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(8),
    specimen_id VARCHAR(8)
);

DO $$
DECLARE
    v_employee_id VARCHAR(8);
    v_specimen_id VARCHAR(8);
BEGIN
    -- Insert a test employee (researcher)
    INSERT INTO employees (employee_id, first_name, last_name, department_id, start_date)
    VALUES ('testing', 'testing', 'testing', 1, CURRENT_DATE)
    RETURNING employee_id INTO v_employee_id;
  
    -- Insert a test specimen
    INSERT INTO specimens (specimen_id, specimen_name, acquisition_date)
    VALUES ('testing', 'testing', CURRENT_DATE)
    RETURNING specimen_id INTO v_specimen_id;

    -- Associate researcher and specimen
    INSERT INTO researcher_specimens (employee_id, specimen_id)
    VALUES (v_employee_id, v_specimen_id);

    -- Capture test IDs
    INSERT INTO test_ids (employee_id, specimen_id)
    VALUES (v_employee_id, v_specimen_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on specimen_id
DELETE FROM specimens WHERE specimen_id = (SELECT specimen_id FROM test_ids);

-- Verify cascading deletion in researcher_specimens
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM researcher_specimens
        WHERE specimen_id = (SELECT specimen_id FROM test_ids)
    ),
    'Deleting a specimen cascades deletion to researcher_specimens'
);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
