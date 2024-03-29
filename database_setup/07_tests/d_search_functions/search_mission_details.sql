SELECT plan(5);
-- Test for exact match
SELECT ok(
    ((SELECT count(*) FROM search_mission_details('Fire')) > 0),
    'Search for "Fire" returns results'
);

-- Test for no matches
SELECT is(
    CAST ((SELECT count(*) FROM search_mission_details('XYZ123')) AS INTEGER),
    0,
    'Search for "XYZ123" returns no results'
);

-- Test for partial match
SELECT ok(
    ((SELECT count(*) FROM search_mission_details('Fir:*')) > 1),
    'Partial search for "Fir" returns multiple results'
);

-- Test for case sensitivity
SELECT ok(
    ((SELECT count(*) FROM search_mission_details('fire')) > 0),
    'Search is case-insensitive'
);

-- Test for special characters
SELECT ok(
    ((SELECT count(*) FROM search_mission_details('planet''s')) > 0),
    'Search for names with special characters returns results'
);

SELECT * FROM finish();