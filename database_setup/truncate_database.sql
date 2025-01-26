DO $$
DECLARE
    r RECORD;
BEGIN
    -- Disable all triggers to avoid foreign key issues during truncation
    PERFORM set_config('session_replication_role', 'replica', true);

    -- Loop through all tables and truncate them
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('TRUNCATE TABLE %I CASCADE', r.tablename);
    END LOOP;

    -- Re-enable triggers
    PERFORM set_config('session_replication_role', 'origin', true);
END $$;
