SELECT plan(4);
-- Test for exact match
SELECT ok(
    ((SELECT count(*) FROM search_origin_details('Uzirp')) > 0),
    'Search for "Uzirp" returns results'
);

-- Test for no matches
SELECT is(
    CAST ((SELECT count(*) FROM search_origin_details('XYZ123')) AS INTEGER),
    0,
    'Search for "XYZ123" returns no results'
);

-- Test for partial match
SELECT ok(
    ((SELECT count(*) FROM search_origin_details('Ic:*')) > 1),
    'Partial search for "Ic" returns multiple results'
);

-- Test for case sensitivity
SELECT ok(
    ((SELECT count(*) FROM search_origin_details('uzirp')) > 0),
    'Search is case-insensitive'
);

SELECT * FROM finish();