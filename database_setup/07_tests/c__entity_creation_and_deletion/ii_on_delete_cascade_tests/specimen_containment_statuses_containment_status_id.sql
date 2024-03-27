BEGIN;
-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL,
    specimen_id VARCHAR(8),
    containment_status_id INTEGER
);

DO $$
DECLARE
    v_specimen_id VARCHAR(8);
    v_containment_status_id INTEGER;
BEGIN
    -- Insert a test specimen
    INSERT INTO specimens (specimen_id, specimen_name, acquisition_date)
    VALUES ('testing', 'testing', CURRENT_DATE)
    RETURNING specimen_id INTO v_specimen_id;
  
    -- Insert a test containment status
    INSERT INTO containment_statuses (status_name, description)
    VALUES ('testing', 'testing')
    RETURNING containment_status_id INTO v_containment_status_id;

    -- Associate specimen and containment status
    INSERT INTO specimen_containment_statuses (specimen_id, containment_status_id)
    VALUES (v_specimen_id, v_containment_status_id);

    -- Capture test IDs
    INSERT INTO test_ids (specimen_id, containment_status_id)
    VALUES (v_specimen_id, v_containment_status_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on containment_status_id
DELETE FROM containment_statuses WHERE containment_status_id = (SELECT containment_status_id FROM test_ids);

-- Verify cascading deletion in specimen_containment_statuses
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM specimen_containment_statuses
        WHERE containment_status_id = (SELECT containment_status_id FROM test_ids)
    ),
    'Deleting a containment status cascades deletion to specimen_containment_statuses'
);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
