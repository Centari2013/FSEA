SELECT plan(5);
-- Test for exact match
SELECT ok(
    ((SELECT count(*) FROM search_employee_details('John')) > 0),
    'Search for "John" returns results'
);

-- Test for no matches
SELECT is(
    CAST ((SELECT count(*) FROM search_employee_details('XYZ123')) AS INTEGER),
    0,
    'Search for "XYZ123" returns no results'
);

-- Test for partial match
SELECT ok(
    ((SELECT count(*) FROM search_employee_details('Joh:*')) > 1),
    'Partial search for "J" returns multiple results'
);

-- Test for case sensitivity
SELECT ok(
    ((SELECT count(*) FROM search_employee_details('john')) > 0),
    'Search is case-insensitive'
);

-- Test for special characters
SELECT ok(
    ((SELECT count(*) FROM search_employee_details('O''Connor')) > 0),
    'Search for names with special characters returns results'
);

SELECT * FROM finish();