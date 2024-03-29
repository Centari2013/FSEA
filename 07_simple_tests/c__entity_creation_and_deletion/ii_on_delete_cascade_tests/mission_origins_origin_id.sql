-- mission_origins_origin_id.sql

BEGIN;

-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL PRIMARY KEY,
    mission_id VARCHAR(8),
    origin_id VARCHAR(8)
);

DO $$
DECLARE
    v_mission_id VARCHAR(8);
    v_origin_id VARCHAR(8);
BEGIN
    -- Insert a test mission
    INSERT INTO missions (mission_id, mission_name, description)
    VALUES ('testing', 'testing', 'testing')
    RETURNING mission_id INTO v_mission_id;

    -- Insert a test origin
    INSERT INTO origins (origin_id, origin_name, discovery_date, description)
    VALUES ('testing', 'testing', CURRENT_DATE, 'testing')
    RETURNING origin_id INTO v_origin_id;


    -- Associate mission and origin
    INSERT INTO mission_origins (mission_id, origin_id)
    VALUES (v_mission_id, v_origin_id);

    -- Capture test IDs
    INSERT INTO test_ids (mission_id, origin_id)
    VALUES (v_mission_id, v_origin_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on origin_id
DELETE FROM origins WHERE origin_id = (SELECT origin_id FROM test_ids);

-- Verify cascading deletion
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM mission_origins
        WHERE origin_id = (SELECT origin_id FROM test_ids)
    ),
    'Deleting an origin cascades deletion on mission_origins'
);

-- Cleanup
DELETE FROM missions WHERE mission_id = (SELECT mission_id FROM test_ids);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
