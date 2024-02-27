CREATE OR REPLACE TRIGGER update_employees_modified
    BEFORE UPDATE
    ON employees
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();



CREATE OR REPLACE TRIGGER update_employeeMedicalRecords_modified
    BEFORE UPDATE
    ON employeeMedicalRecords
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();



CREATE OR REPLACE TRIGGER update_missions_modified
    BEFORE UPDATE
    ON missions
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();



CREATE OR REPLACE TRIGGER update_specimens_modified
    BEFORE UPDATE
    ON specimens
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();



CREATE OR REPLACE TRIGGER update_specimenMedicalRecords_modified
    BEFORE UPDATE
    ON specimenMedicalRecords
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();



CREATE OR REPLACE TRIGGER update_origins_modified
    BEFORE UPDATE
    ON origins
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();



CREATE OR REPLACE TRIGGER update_credentials_modified
    BEFORE UPDATE
    ON credentials
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();



CREATE OR REPLACE TRIGGER create_employee_records
    AFTER INSERT
    ON employees
    FOR EACH ROW
    EXECUTE FUNCTION create_employee_records();



CREATE OR REPLACE TRIGGER create_specimen_medical_record
    AFTER INSERT
    ON specimens
    FOR EACH ROW
    EXECUTE FUNCTION create_specimen_medical_record();



CREATE OR REPLACE TRIGGER insert_employeeID
    BEFORE INSERT
    ON employees
    FOR EACH ROW
    EXECUTE FUNCTION insert_employeeID();

CREATE OR REPLACE TRIGGER insert_specimenID
    BEFORE INSERT
    ON specimens
    FOR EACH ROW
    EXECUTE FUNCTION insert_specimenID();

CREATE OR REPLACE TRIGGER insert_originID
    BEFORE INSERT
    ON origins
    FOR EACH ROW
    EXECUTE FUNCTION insert_originID();

CREATE OR REPLACE TRIGGER insert_missionID
    BEFORE INSERT
    ON missions
    FOR EACH ROW
    EXECUTE FUNCTION insert_missionID();
