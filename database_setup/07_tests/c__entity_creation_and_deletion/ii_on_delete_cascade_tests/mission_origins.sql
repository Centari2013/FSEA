-- All of the following tests are contingent upon the fact that the trigger test have run successfully.
-- Mission and Origin creations will be inserted into the mission_origins table.
-- Missionand Origin deletions are supposed to remove those foreign key links from the mission_origins table.
SELECT plan(10);

-- mission_origins origins(origin_id) on delete cascade
-- create mission
SELECT lives_ok(
    'INSERT INTO missions (mission_name, description)
    VALUES (''testing'', ''testing'')',
    'missions insertion success.'
    );

-- create origin
SELECT lives_ok(
    'INSERT INTO origins (origin_name, discovery_date, description)
    VALUES (''testing'', CURRENT_DATE, ''testing'')',
    'missions insertion success.'
    );
-- delete origin
SELECT lives_ok(
    'DELETE FROM origins WHERE origin_name = ''testing''',
    'origins cleanup success.'
);
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM employee_clearances ec
        JOIN employees e ON ec.employee_id = e.employee_id
        WHERE e.first_name = 'testing'
        ),
        'employees cascade deletion on employee_clearances success.');
-- cleanup clearance
SELECT lives_ok(
    'DELETE FROM clearances WHERE clearance_name = ''testing''',
    'clearances cleanup success.'
);




SELECT * FROM finish();