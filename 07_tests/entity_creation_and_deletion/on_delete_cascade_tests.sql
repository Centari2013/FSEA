SELECT plan();

-- employee_clearances clearances(clearance_id) on delete cascade
SELECT lives_ok(
    NOT EXISTS (
        WITH created_employee_id AS ()
        WITH deleted_employee_id AS (
            DELETE FROM clearances WHERE clearance_name = 'testing'
            RETURNING clearance_id
        )
        SELECT 1 FROM employee_clearances WHERE clearance_id = deleted_clearance_id
        
    ),
    'clearances cascade deletion on employee_clearances success.'
);


-- employee_clearances clearances(clearance_id) on delete cascade
SELECT lives_ok(
    NOT EXISTS (
        WITH deleted_clearance_id AS (
            DELETE FROM clearances WHERE clearance_name = 'testing'
            RETURNING clearance_id
        )
        SELECT 1 FROM employee_clearances WHERE clearance_id = deleted_clearance_id
        
    ),
    'clearances cascade deletion on employee_clearances success.'
);
