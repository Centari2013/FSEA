CREATE OR REPLACE TRIGGER update_employees_modified
    BEFORE UPDATE ON employees
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE OR REPLACE TRIGGER update_employee_medical_records_modified
    BEFORE UPDATE ON employee_medical_records
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE OR REPLACE TRIGGER update_missions_modified
    BEFORE UPDATE ON missions
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE OR REPLACE TRIGGER update_specimens_modified
    BEFORE UPDATE ON specimens
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE OR REPLACE TRIGGER update_specimen_medical_records_modified
    BEFORE UPDATE ON specimen_medical_records
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE OR REPLACE TRIGGER update_origins_modified
    BEFORE UPDATE ON origins
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE OR REPLACE TRIGGER update_credentials_modified
    BEFORE UPDATE ON credentials
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE OR REPLACE TRIGGER create_employee_records
    AFTER INSERT ON employees
    FOR EACH ROW
    EXECUTE FUNCTION create_employee_records();

CREATE OR REPLACE TRIGGER create_specimen_medical_record
    AFTER INSERT ON specimens
    FOR EACH ROW
    EXECUTE FUNCTION create_specimen_medical_record();

CREATE OR REPLACE TRIGGER insert_employee_id
    BEFORE INSERT ON employees
    FOR EACH ROW
    EXECUTE FUNCTION insert_employee_id();

CREATE OR REPLACE TRIGGER insert_specimen_id
    BEFORE INSERT ON specimens
    FOR EACH ROW
    EXECUTE FUNCTION insert_specimen_id();

CREATE OR REPLACE TRIGGER insert_origin_id
    BEFORE INSERT ON origins
    FOR EACH ROW
    EXECUTE FUNCTION insert_origin_id();

CREATE OR REPLACE TRIGGER insert_mission_id
    BEFORE INSERT ON missions
    FOR EACH ROW
    EXECUTE FUNCTION insert_mission_id();