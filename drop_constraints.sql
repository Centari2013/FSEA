DO $$ 
DECLARE
    r RECORD; -- Explicitly declare the loop variable as a record type
BEGIN
    -- Loop through all foreign key constraints and drop them
    FOR r IN
        SELECT conname AS constraint_name, conrelid::regclass AS table_name
        FROM pg_constraint
        WHERE contype = 'f'
    LOOP
        EXECUTE format('ALTER TABLE %s DROP CONSTRAINT %I', r.table_name, r.constraint_name);
    END LOOP;
END $$;
