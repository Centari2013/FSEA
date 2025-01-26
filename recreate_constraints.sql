-- Example: Recreate foreign key constraints
ALTER TABLE employee_clearances
ADD CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES employees(employee_id);

ALTER TABLE employee_designations
ADD CONSTRAINT fk_designation FOREIGN KEY (designation_id) REFERENCES designations(designation_id);

-- Repeat for all your constraints
