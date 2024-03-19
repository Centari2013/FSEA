-- Indexes for employees table
CREATE INDEX idx_employees_department_id ON employees(department_id);

-- Indexes for employee related relationships
CREATE INDEX idx_employee_clearances_clearance_id ON employee_clearances(clearance_id);
CREATE INDEX idx_employee_clearances_employee_id ON employee_clearances(employee_id);
CREATE INDEX idx_employee_designations_designation_id ON employee_designations(designation_id);
CREATE INDEX idx_employee_designations_employee_id ON employee_designations(employee_id);
CREATE INDEX idx_employee_missions_mission_id ON employee_missions(mission_id);
CREATE INDEX idx_employee_missions_employee_id ON employee_missions(employee_id);

-- Indexes for missions and related tables
CREATE INDEX idx_missions_commander_id ON missions(commander_id);
CREATE INDEX idx_missions_supervisor_id ON missions(supervisor_id);
CREATE INDEX idx_mission_origins_origin_id ON mission_origins(origin_id);
CREATE INDEX idx_mission_origins_mission_id ON mission_origins(mission_id);

-- Indexes for specimens and related tables
CREATE INDEX idx_specimens_origin_id ON specimens(origin_id);
CREATE INDEX idx_specimens_mission_id ON specimens(mission_id);
CREATE INDEX idx_specimen_containment_statuses_containment_status_id ON specimen_containment_statuses(containment_status_id);
CREATE INDEX idx_specimen_containment_statuses_specimen_id ON specimen_containment_statuses(specimen_id);
CREATE INDEX idx_specimen_missions_specimen_id ON specimen_missions(specimen_id);
CREATE INDEX idx_specimen_missions_mission_id ON specimen_missions(mission_id);

-- Indexes for department missions and employee missions
CREATE INDEX idx_department_missions_department_id ON department_missions(department_id);
CREATE INDEX idx_department_missions_mission_id ON department_missions(mission_id);

-- Indexes for researcher specimens
CREATE INDEX idx_researcher_specimens_employee_id ON researcher_specimens(employee_id);
CREATE INDEX idx_researcher_specimens_specimen_id ON researcher_specimens(specimen_id);


-- TSVECTORS
ALTER TABLE employees
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
    TO_TSVECTOR('english', first_name || ' ' || last_name || ' ' || employee_id)
) STORED;

ALTER TABLE departments
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
    TO_TSVECTOR('english', department_name || ' ' || COALESCE(director_id, '') || ' ' || COALESCE(description, ''))
) STORED;

ALTER TABLE designations
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
    TO_TSVECTOR('english', designation_name || ' ' || abbreviation)
) STORED;

ALTER TABLE missions
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
    TO_TSVECTOR('english', 
        mission_id || ' ' || 
        COALESCE(commander_id, '') || ' ' || 
        COALESCE(supervisor_id, '') || ' ' || 
        mission_name || ' ' || 
        COALESCE(description, '') || ' ' || 
        COALESCE(notes, '')
    )
) STORED;

ALTER TABLE specimens
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
    TO_TSVECTOR('english', specimen_name || ' ' || COALESCE(description, '') || ' ' || COALESCE(notes::text, ''))
) STORED;


CREATE INDEX idx_employees_search_vector ON employees USING GIN(search_vector);
CREATE INDEX idx_departments_search_vector ON departments USING GIN(search_vector);
CREATE INDEX idx_designations_search_vector ON designations USING GIN(search_vector);
CREATE INDEX idx_missions_search_vector ON missions USING GIN(search_vector);
CREATE INDEX idx_specimens_search_vector ON specimens USING GIN(search_vector);
