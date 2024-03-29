CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_employee_records()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO employee_medical_records (employee_id) 
    VALUES (NEW.employee_id);

    INSERT INTO credentials (employee_id) 
    VALUES (NEW.employee_id);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_specimen_medical_record()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO specimen_medical_records (specimen_id) 
    VALUES (NEW.specimen_id);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION generate_unique_id(prefix TEXT, target_table TEXT, target_column TEXT)
RETURNS TEXT AS $$
DECLARE
    new_id TEXT;
    id_exists INTEGER;
    query TEXT;
BEGIN
    LOOP
        -- Generate the ID with the provided prefix
        new_id := prefix || LPAD(CAST(FLOOR(RANDOM() * 9999999) AS TEXT), 7, '0');

        -- Create a dynamic SQL query to check if the generated ID exists
        query := format('SELECT COUNT(*) FROM %I WHERE %I = $1', target_table, target_column);

        -- Execute the dynamic SQL query
        EXECUTE query INTO id_exists USING new_id;

        -- If not found, return the new ID
        IF id_exists = 0 THEN
            RETURN new_id;
        END IF;
        -- If found, the loop will continue and generate a new ID
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_employee_id()
RETURNS TRIGGER AS $$
BEGIN
    NEW.employee_id := generate_unique_id('E', 'employees', 'employee_id');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_specimen_id()
RETURNS TRIGGER AS $$
BEGIN
    NEW.specimen_id := generate_unique_id('S', 'specimens', 'specimen_id');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_mission_id()
RETURNS TRIGGER AS $$
BEGIN
    NEW.mission_id := generate_unique_id('M', 'missions', 'mission_id');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_origin_id()
RETURNS TRIGGER AS $$
BEGIN
    NEW.origin_id := generate_unique_id('O', 'origins', 'origin_id');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;