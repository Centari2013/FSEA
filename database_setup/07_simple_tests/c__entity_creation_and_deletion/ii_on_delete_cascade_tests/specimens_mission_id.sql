BEGIN;

-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL,
    specimen_id VARCHAR(8),
    mission_id VARCHAR(8)
);

DO $$
DECLARE
    v_specimen_id VARCHAR(8);
    v_mission_id VARCHAR(8);
BEGIN
    -- Insert a test mission
    INSERT INTO missions (mission_id, mission_name, description)
    VALUES ('testing', 'testing', 'testing')
    RETURNING mission_id INTO v_mission_id;
  
    -- Insert a test specimen linked to the test mission
    INSERT INTO specimens (specimen_id, specimen_name, mission_id, acquisition_date)
    VALUES ('testing', 'testing', v_mission_id, CURRENT_DATE)
    RETURNING specimen_id INTO v_specimen_id;

    -- Capture test IDs
    INSERT INTO test_ids (specimen_id, mission_id)
    VALUES (v_specimen_id, v_mission_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on mission_id
DELETE FROM missions WHERE mission_id = (SELECT mission_id FROM test_ids);

-- Verify cascading deletion in specimens
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM specimens
        WHERE mission_id = (SELECT mission_id FROM test_ids)
    ),
    'Deleting a mission cascades deletion to specimens'
);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
