SELECT plan(4);
-- Test for exact match
SELECT ok(
    ((SELECT count(*) FROM search_department_details('Executive')) > 0),
    'Search for "Alex" returns results'
);

-- Test for no matches
SELECT is(
    CAST ((SELECT count(*) FROM search_department_details('XYZ123')) AS INTEGER),
    0,
    'Search for "XYZ123" returns no results'
);

-- Test for partial match
SELECT ok(
    ((SELECT count(*) FROM search_department_details('Exec:*')) > 0),
    'Partial search for "Exec" returns partial match results'
);

-- Test for case sensitivity
SELECT ok(
    ((SELECT count(*) FROM search_department_details('executive')) > 0),
    'Search is case-insensitive'
);


SELECT * FROM finish();