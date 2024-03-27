BEGIN;

-- Create test data
CREATE TEMP TABLE test_ids (
    id SERIAL PRIMARY KEY,
    specimen_id VARCHAR(8)
);

DO $$
DECLARE
    v_specimen_id VARCHAR(8);
BEGIN
    -- Insert a test specimen
    INSERT INTO specimens (specimen_id, specimen_name, acquisition_date)
    VALUES ('testing', 'testing', CURRENT_DATE)
    RETURNING specimen_id INTO v_specimen_id;
  
    -- Insert a test specimen medical record linked to the test specimen
    INSERT INTO specimen_medical_records (specimen_id, bloodtype, kilograms, height_cm)
    VALUES (v_specimen_id, 'O+', 70.0, 180.0);

    -- Capture test ID
    INSERT INTO test_ids (specimen_id)
    VALUES (v_specimen_id);

END;
$$;

-- Plan the tests
SELECT plan(1);

-- Test cascading delete on specimen_id
DELETE FROM specimens WHERE specimen_id = (SELECT specimen_id FROM test_ids);

-- Verify cascading deletion in specimen_medical_records
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM specimen_medical_records
        WHERE specimen_id = (SELECT specimen_id FROM test_ids)
    ),
    'Deleting a specimen cascades deletion to specimen_medical_records'
);

-- Finish the tests
SELECT * FROM finish();

ROLLBACK;
