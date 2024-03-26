BEGIN;
SELECT plan(11);

-- test cases

-- update_employees_modified
UPDATE employees SET first_name = 'Centari' WHERE employee_id = 'E7449700';
SELECT ok (
    (SELECT EXTRACT(EPOCH FROM (NOW() - updated)) < 60 FROM employees WHERE employee_id = 'E7449700'),
    'update_employees_modified trigger correctly updates the updated column.'
);

-- update_employee_medical_records_modified
UPDATE employee_medical_records SET sex = 'm' WHERE employee_id = 'E7449700';
SELECT ok (
    (SELECT EXTRACT(EPOCH FROM (NOW() - updated)) < 60 FROM employee_medical_records WHERE employee_id = 'E7449700'),
    'update_employee_medical_records_modified trigger correctly updates the updated column.'
);

-- update_missions_modified
UPDATE missions SET mission_name = 'testing' WHERE mission_id = 'M9093853';
SELECT ok (
    (SELECT EXTRACT(EPOCH FROM (NOW() - updated)) < 60 FROM missions WHERE mission_id = 'M9093853'),
    'update_missions_modified trigger correctly updates the updated column.'
);

-- update_specimens_modified
UPDATE specimens SET specimen_name = 'testing' WHERE specimen_id = 'S2015640';
SELECT ok (
    (SELECT EXTRACT(EPOCH FROM (NOW() - updated)) < 60 FROM specimens WHERE specimen_id = 'S2015640'),
    'update_specimens_modified trigger correctly updates the updated column.'
);

-- update_specimen_medical_records_modified
UPDATE specimen_medical_records SET sex = 'intersex' WHERE specimen_id = 'S2015640';
SELECT ok (
    (SELECT EXTRACT(EPOCH FROM (NOW() - updated)) < 60 FROM specimen_medical_records WHERE specimen_id = 'S2015640'),
    'update_specimen_medical_records_modified trigger correctly updates the updated column.'
);

-- update_origins_modified
UPDATE origins SET origin_name = 'testing' WHERE origin_id = 'O2366904';
SELECT ok (
    (SELECT EXTRACT(EPOCH FROM (NOW() - updated)) < 60 FROM origins WHERE origin_id = 'O2366904'),
    'update_origins_modified trigger correctly updates the updated column.'
);

-- update_credentials_modified
UPDATE credentials SET username = 'testing' WHERE employee_id = 'E7449700';
SELECT ok (
    (SELECT EXTRACT(EPOCH FROM (NOW() - updated)) < 60 FROM credentials WHERE employee_id = 'E7449700'),
    'update_credentials_modified trigger correctly updates the updated column.'
);

-- insert_employee_id
WITH inserted_employee AS (
    INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES ('testing', 'testing', 1, CURRENT_DATE)
    RETURNING employee_id
)
SELECT ok(
    (SELECT employee_id FROM inserted_employee) SIMILAR TO 'E[0-9]{7}',
    'employee_id is correctly generated with format E and 7 numbers.'
);

-- insert_specimen_id
WITH inserted_specimen AS (
    INSERT INTO specimens (specimen_name, acquisition_date)
    VALUES ('testing', CURRENT_DATE)
    RETURNING specimen_id
)
SELECT ok(
    (SELECT specimen_id FROM inserted_specimen) SIMILAR TO 'S[0-9]{7}',
    'specimen_id is correctly generated with format S and 7 numbers.'
);
-- insert_origin_id
WITH inserted_origin AS (
    INSERT INTO origins (origin_name, discovery_date, description)
    VALUES ('name', CURRENT_DATE, 'desc')
    RETURNING origin_id
)
SELECT ok(
    (SELECT origin_id FROM inserted_origin) SIMILAR TO 'O[0-9]{7}',
   'origin_id is correctly generated with format O and 7 numbers.'
);

-- insert_mission_id
WITH inserted_mission AS (
    INSERT INTO missions (mission_name, description)
    VALUES ('name', 'desc')
    RETURNING mission_id
)
SELECT ok(
    (SELECT mission_id FROM inserted_mission) SIMILAR TO 'M[0-9]{7}',
    'mission_id is correctly generated with format M and 7 numbers.'
);

SELECT * FROM finish();
ROLLBACK;



