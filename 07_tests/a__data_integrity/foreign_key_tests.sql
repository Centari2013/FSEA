-- initialize test plan with num of tests
SELECT plan(25);

-- test cases

-- departments fk_director_id
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM departments WHERE director_id IS NOT NULL AND director_id NOT IN (
            SELECT employee_id FROM employees
        )
    ),
    'All departments director_id valid.'
);

-- employees_department_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employees WHERE department_id NOT IN (
            SELECT department_id FROM departments
        )
    ),
    'All employees department_id valid.'
);

-- employee_clearances_clearance_id_fk
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_clearances WHERE clearance_id NOT IN (
            SELECT clearance_id FROM clearances
        )
    ),
    'All employee_clearances clearance_id valid.'
);


-- employee_clearances_employee_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_clearances WHERE employee_id NOT IN (
            SELECT employee_id FROM employees
        )
    ),
    'All employee_clearances employee_id valid.'
);

-- employee_designations_designation_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_designations WHERE designation_id NOT IN (
            SELECT designation_id FROM designations
        )
    ),
    'All employee_designations designation_id valid.' 
);

-- employee_designations_employee_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_designations WHERE employee_id NOT IN (
            SELECT employee_id FROM employees
        )
    ),
    'All employee_designations employee_id valid.' 
);

-- employee_medical_records_employee_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_medical_records WHERE employee_id NOT IN (
            SELECT employee_id FROM employees
        )
    ),
    'All employee_medical_records employee_id valid.'
);

-- missions_commander_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM missions WHERE commander_id IS NOT NULL AND commander_id NOT IN (
            SELECT employee_id FROM employees
        )
    ),
    'All missions commander_id valid.'
);

-- missions_supervisor_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM missions WHERE supervisor_id IS NOT NULL AND supervisor_id NOT IN (
            SELECT employee_id FROM employees
        )
    ),
    'All missions supervisor_id valid.'
);

-- mission_origins_mission_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM mission_origins WHERE mission_id NOT IN (
            SELECT mission_id FROM missions
        )
    ),
    'All mission_origins mission_id valid.'
);

-- missions_origins_origin_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM mission_origins WHERE origin_id NOT IN (
            SELECT origin_id FROM origins
        )
    ),
    'All mission_origins origin_id valid.'
);

-- specimens_mission_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM specimens WHERE mission_id NOT IN (
            SELECT mission_id FROM missions
        )
    ),
    'All specimens mission_id valid.'
);

-- specimens_origin_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM specimens WHERE origin_id NOT IN (
            SELECT origin_id FROM origins
        )
    ),
    'All specimens origin_id valid.'
);

-- specimen_containment_statuses_status_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM specimen_containment_statuses WHERE containment_status_id NOT IN (
            SELECT containment_status_id FROM containment_statuses
        )
    ),
    'All specimen_containment_statuses status_id valid.'
);

-- specimen_containment_statuses_specimen_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM specimen_containment_statuses WHERE specimen_id NOT IN (
            SELECT specimen_id FROM specimens
        )
    ),
    'All specimen_containment_statuses specimen_id valid.'
);

-- specimen_medical_records_specimen_id
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM specimen_medical_records WHERE specimen_id NOT IN (
            SELECT specimen_id FROM specimens
        )
    ),
    'All specimen_medical_records specimen_id valid.'
);


-- specimen_missions_mission_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM specimen_missions WHERE mission_id NOT IN (
            SELECT mission_id FROM missions
        )
    ),
    'All specimen_missions mission_id valid.'
);

-- specimen_missions_specimen_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM specimen_missions WHERE specimen_id NOT IN (
            SELECT specimen_id FROM specimens
        )
    ),
    'All specimen_missions specimen_id valid.'
);


-- credentials_employee_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM credentials WHERE employee_id NOT IN (
            SELECT employee_id FROM employees
        )
    ),
    'All credentials employee_id valid.'
);

-- department_missions_department_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM department_missions WHERE department_id NOT IN (
            SELECT department_id FROM departments
        )
    ),
    'All department_missions department_id valid.'
);

-- department_missions_mission_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM department_missions WHERE mission_id NOT IN (
            SELECT mission_id FROM missions
        )
    ),
    'All department_missions mission_id valid.'
);

-- employee_missions_employee_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_missions WHERE employee_id NOT IN (
            SELECT employee_id FROM employees
        )
    ),
    'All employee_missions employee_id valid.'
);


-- employee_missions_mission_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM employee_missions WHERE mission_id NOT IN (
            SELECT mission_id FROM missions
        )
    ),
    'All employee_missions mission_id valid.'
);

-- researcher_specimens_employee_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM researcher_specimens WHERE employee_id NOT IN (
            SELECT employee_id FROM employees
        )
    ),
    'All researcher_specimens employee_id valid.'
);

-- researcher_specimens_specimen_id_fkey
SELECT ok (
    NOT EXISTS (
        SELECT 1 FROM researcher_specimens WHERE specimen_id NOT IN (
            SELECT specimen_id FROM specimens
        )
    ),
    'All researcher_specimens specimen_id valid.'
);


-- finish tests
SELECT * FROM finish();