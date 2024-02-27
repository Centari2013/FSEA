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
        INSERT INTO employeeMedicalRecords(employeeID) VALUES (NEW.employeeID);
        INSERT INTO credentials(employeeID) VALUES (NEW.employeeID);
        RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION create_specimen_medical_record()
RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO specimenMedicalRecords(specimenID) VALUES (NEW.specimenID);
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



CREATE OR REPLACE FUNCTION insert_employeeID()
RETURNS TRIGGER AS $$
BEGIN
    NEW.employeeID := generate_unique_id('E', 'employees', 'employeeID');
END;

$$ LANGUAGE  plpgsql;



CREATE OR REPLACE FUNCTION insert_specimenID()
RETURNS TRIGGER AS $$
BEGIN
    NEW.specimenID := generate_unique_id('S', 'specimens', 'specimenID');
END;

$$ LANGUAGE  plpgsql;



CREATE OR REPLACE FUNCTION insert_missionID()
RETURNS TRIGGER AS $$
BEGIN
    NEW.missionID := generate_unique_id('M', 'missions', 'missionID');
END;

$$ LANGUAGE  plpgsql;



CREATE OR REPLACE FUNCTION insert_originID()
RETURNS TRIGGER AS $$
BEGIN
    NEW.originID := generate_unique_id('O', 'origins', 'originID');
END;

$$ LANGUAGE  plpgsql;






