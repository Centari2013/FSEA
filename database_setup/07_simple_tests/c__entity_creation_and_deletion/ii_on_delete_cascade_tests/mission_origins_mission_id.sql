BEGIN;

-- create test data
CREATE TEMP TABLE test_ids (
    id SERIAL,
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
  
   
    INSERT INTO origins (origin_id, origin_name, discovery_date, description)
    VALUES ('testing', 'testing', CURRENT_DATE, 'testing')
    RETURNING origin_id INTO v_origin_id;

   
    INSERT INTO mission_origins (mission_id, origin_id)
    VALUES (v_mission_id, v_origin_id);

   
    INSERT INTO test_ids (mission_id, origin_id)
    VALUES (v_mission_id, v_origin_id);

END;
$$;


SELECT plan(1);

-- cascading delete on mission_id
DELETE FROM missions WHERE mission_id = (SELECT mission_id FROM test_ids);

-- verify cascading deletion
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM mission_origins
        WHERE mission_id = (SELECT mission_id FROM test_ids)
    ),
    'Deleting a mission cascades deletion on mission_origins'
);

-- cleanup
DELETE FROM origins WHERE origin_id = (SELECT origin_id FROM test_ids);


SELECT * FROM finish();

ROLLBACK;
