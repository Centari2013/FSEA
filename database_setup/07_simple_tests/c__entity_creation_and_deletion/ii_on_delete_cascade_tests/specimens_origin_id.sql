BEGIN;

-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL ,
    specimen_id VARCHAR(8),
    origin_id VARCHAR(8)
);

DO $$
DECLARE
    v_specimen_id VARCHAR(8);
    v_origin_id VARCHAR(8);
BEGIN
    -- Insert a test origin
    INSERT INTO origins (origin_id, origin_name, discovery_date, description)
    VALUES ('testing', 'testing', CURRENT_DATE, 'testing')
    RETURNING origin_id INTO v_origin_id;
  
    -- Insert a test specimen linked to the test origin
    INSERT INTO specimens (specimen_id, specimen_name, origin_id, acquisition_date)
    VALUES ('testing', 'testing', v_origin_id, CURRENT_DATE)
    RETURNING specimen_id INTO v_specimen_id;

    -- Capture test IDs
    INSERT INTO test_ids (specimen_id, origin_id)
    VALUES (v_specimen_id, v_origin_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on origin_id
DELETE FROM origins WHERE origin_id = (SELECT origin_id FROM test_ids);

-- Verify cascading deletion in specimens
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM specimens
        WHERE origin_id = (SELECT origin_id FROM test_ids)
    ),
    'Deleting an origin cascades deletion to specimens'
);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
