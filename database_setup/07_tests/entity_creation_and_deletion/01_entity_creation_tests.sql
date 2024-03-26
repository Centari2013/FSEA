
SELECT plan();

-- create clearance
SELECT lives_ok(
    'INSERT INTO clearances ()',
    'clearances insertion success.'
)