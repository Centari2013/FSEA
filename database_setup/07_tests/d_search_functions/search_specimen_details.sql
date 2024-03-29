SELECT plan(4);
-- Test for exact match
SELECT ok(
    ((SELECT count(*) FROM search_specimen_details('Toxic')) > 0),
    'Search for "John" returns results'
);

-- Test for no matches
SELECT is(
    CAST ((SELECT count(*) FROM search_specimen_details('XYZ123')) AS INTEGER),
    0,
    'Search for "XYZ123" returns no results'
);

-- Test for partial match
SELECT ok(
    ((SELECT count(*) FROM search_specimen_details('Tox:*')) > 1),
    'Partial search for "Tox" returns multiple results'
);

-- Test for case sensitivity
SELECT ok(
    ((SELECT count(*) FROM search_specimen_details('toxic')) > 0),
    'Search is case-insensitive'
);


SELECT * FROM finish();