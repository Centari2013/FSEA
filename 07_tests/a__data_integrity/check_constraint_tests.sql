BEGIN;
SELECT plan(6);

-- test cases

-- employee_medical_records_bloodtype_check
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_medical_records WHERE bloodtype NOT IN (
           'A+', 'O+', 'B+', 'AB+', 'A-', 'O-', 'B-', 'AB-', 'V-', 'V+', 'BF', 'undefined' 
        )
    ),
    'All employee_medical_records bloodtype valid.'
);

-- employee_medical_records_height_cm_check
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_medical_records WHERE height_cm <= 0
    ),
    'All employee_medical_records height_cm valid.'
);

-- employee_medical_records_sex_check
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_medical_records WHERE sex NOT IN (
            'm', 'f', 'inter', 'unknown', 'undefined'
        )
    ),
    'All employee_medical_records sex valid.'
);

-- employee_medical_records_kilograms_check
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_medical_records WHERE kilograms <= 0
    ),
    'All employee_medical_records kilograms valid.'
);

-- specimens_threat_level_check
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM specimens WHERE threat_level < 0 OR threat_level > 10
    ),
    'All specimens threat_level valid.'
);

-- specimen_medical_records_kilograms_check
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM specimen_medical_records WHERE kilograms <= 0
    ),
    'All specimen_medical_records kilograms valid.'
);

SELECT * FROM finish();
ROLLBACK;