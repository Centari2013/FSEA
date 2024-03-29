BEGIN;

-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL PRIMARY KEY,
    specimen_id VARCHAR(8),
    mission_id VARCHAR(8)
);

DO $$
DECLARE
    v_specimen_id VARCHAR(8);
    v_mission_id VARCHAR(8);
BEGIN
    -- Insert a test specimen
    INSERT INTO specimens (specimen_id, specimen_name, acquisition_date)
    VALUES ('testing', 'testing', CURRENT_DATE)
    RETURNING specimen_id INTO v_specimen_id;
  
    -- Insert a test mission
    INSERT INTO missions (mission_id, mission_name, description)
    VALUES ('testing', 'testing', 'testing')
    RETURNING mission_id INTO v_mission_id;

    -- Associate specimen and mission
    INSERT INTO specimen_missions (specimen_id, mission_id, involvement_summary)
    VALUES (v_specimen_id, v_mission_id, 'testing');

    -- Capture test IDs
    INSERT INTO test_ids (specimen_id, mission_id)
    VALUES (v_specimen_id, v_mission_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on specimen_id
DELETE FROM specimens WHERE specimen_id = (SELECT specimen_id FROM test_ids);

-- Verify cascading deletion in specimen_missions
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM specimen_missions
        WHERE specimen_id = (SELECT specimen_id FROM test_ids)
    ),
    'Deleting a specimen cascades deletion to specimen_missions'
);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
