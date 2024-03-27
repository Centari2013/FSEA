CREATE TABLE clearances (
    clearance_id SERIAL PRIMARY KEY,
    clearance_name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE containment_statuses (
    containment_status_id SERIAL PRIMARY KEY,
    status_name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name TEXT NOT NULL,
    director_id VARCHAR(8), -- Assuming employeeID types for consistency
    description TEXT DEFAULT NULL
);

CREATE TABLE designations (
    designation_id SERIAL PRIMARY KEY,
    designation_name TEXT NOT NULL,
    abbreviation VARCHAR(5) NOT NULL
);



CREATE TABLE employees (
    employee_id VARCHAR(8) PRIMARY KEY, -- Employee IDs are formatted as 'EXXXXXXX'
    department_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE DEFAULT NULL,
    notes JSONB DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE employee_clearances (
    employee_id VARCHAR(8),
    clearance_id INTEGER,
    PRIMARY KEY (employee_id, clearance_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (clearance_id) REFERENCES clearances(clearance_id) ON DELETE CASCADE
);

CREATE TABLE employee_designations (
    employee_id VARCHAR(8),
    designation_id INTEGER NOT NULL,
    PRIMARY KEY (employee_id, designation_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (designation_id) REFERENCES designations(designation_id)
);

CREATE TABLE employee_medical_records (
    employee_id VARCHAR(8) PRIMARY KEY,
    dob DATE,
    bloodtype VARCHAR(10) DEFAULT NULL CHECK (bloodtype IN ('A+', 'O+', 'B+', 'AB+', 'A-', 'O-', 'B-', 'AB-', 'V-', 'V+', 'BF', 'undefined')),
    sex VARCHAR(10) DEFAULT NULL CHECK (sex IN ('m', 'f', 'inter', 'unknown', 'undefined')),
    kilograms REAL CHECK(kilograms > 0),
    height_cm REAL CHECK (height_cm > 0),
    notes JSONB DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

CREATE TABLE missions (
    mission_id VARCHAR(8) PRIMARY KEY, -- Mission IDs are formatted as 'MXXXXXXX'
    mission_name TEXT NOT NULL DEFAULT 'NAME-PENDING',
    start_date DATE,
    end_date DATE,
    commander_id VARCHAR(8),
    supervisor_id VARCHAR(8),
    description TEXT NOT NULL,
    notes JSONB DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (commander_id) REFERENCES employees(employee_id),
    FOREIGN KEY (supervisor_id) REFERENCES employees(employee_id) 
);

CREATE TABLE origins (
    origin_id VARCHAR(8) PRIMARY KEY, -- Origin IDs are formatted as 'OXXXXXXX'
    origin_name TEXT NOT NULL,
    discovery_date DATE NOT NULL,
    description TEXT NOT NULL,
    notes JSONB DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL
);

CREATE TABLE mission_origins (
    mission_id VARCHAR(8) NOT NULL,
    origin_id VARCHAR(8) NOT NULL,
    PRIMARY KEY (mission_id, origin_id),
    FOREIGN KEY (origin_id) REFERENCES origins(origin_id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES missions(mission_id) ON DELETE CASCADE
);

CREATE TABLE specimens (
    specimen_id VARCHAR(8) PRIMARY KEY, -- SpecimenIDs are formatted as 'SXXXXXXX'
    specimen_name TEXT NOT NULL,
    origin_id VARCHAR(8),
    mission_id VARCHAR(8),
    threat_level REAL CHECK (threat_level >= 0 AND threat_level <= 10),
    acquisition_date DATE NOT NULL,
    notes JSONB DEFAULT NULL,
    description TEXT DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (origin_id) REFERENCES origins(origin_id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES missions(mission_id) ON DELETE CASCADE
);

CREATE TABLE specimen_containment_statuses (
    specimen_id VARCHAR(8) NOT NULL,
    containment_status_id INTEGER,
    PRIMARY KEY (specimen_id, containment_status_id),
    FOREIGN KEY (specimen_id) REFERENCES specimens(specimen_id) ON DELETE CASCADE,
    FOREIGN KEY (containment_status_id) REFERENCES containment_statuses(containment_status_id) ON DELETE CASCADE
);

CREATE TABLE specimen_medical_records (
    specimen_id VARCHAR(8) PRIMARY KEY,
    bloodtype VARCHAR(10) DEFAULT NULL,
    sex VARCHAR(10) DEFAULT NULL,
    kilograms REAL CHECK(kilograms > 0),
    notes JSONB DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (specimen_id) REFERENCES specimens(specimen_id) ON DELETE CASCADE
);

CREATE TABLE specimen_missions (
    specimen_id VARCHAR(8) NOT NULL,
    mission_id VARCHAR(8) NOT NULL,
    involvement_summary TEXT,
    PRIMARY KEY (specimen_id, mission_id),
    FOREIGN KEY (specimen_id) REFERENCES specimens(specimen_id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES missions(mission_id) ON DELETE CASCADE
);

CREATE TABLE credentials (
    employee_id VARCHAR(8) PRIMARY KEY,
    username TEXT DEFAULT NULL,
    password TEXT DEFAULT NULL,
    login_attempts INTEGER DEFAULT 0,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

CREATE TABLE department_missions (
    department_id INTEGER NOT NULL,
    mission_id VARCHAR(8) NOT NULL,
    PRIMARY KEY (department_id, mission_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES missions(mission_id) ON DELETE CASCADE
);

CREATE TABLE employee_missions (
    employee_id VARCHAR(8) NOT NULL,
    mission_id VARCHAR(8) NOT NULL,
    involvement_summary TEXT DEFAULT NULL,
    PRIMARY KEY (employee_id, mission_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES missions(mission_id) ON DELETE CASCADE
);

CREATE TABLE researcher_specimens (
    employee_id VARCHAR(8) NOT NULL,
    specimen_id VARCHAR(8) NOT NULL,
    PRIMARY KEY (employee_id, specimen_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (specimen_id) REFERENCES specimens(specimen_id) ON DELETE CASCADE
);
-- employee_clearances clearances(clearance_id) on delete cascade
WITH created_employee AS (
    INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES ('testing', 'testing', 1, CURRENT_DATE)
    RETURNING employee_id
), deleted_employee_id AS (
    DELETE FROM employees
    WHERE employee_id IN (SELECT employee_id FROM created_employee)
    RETURNING employee_id
)
SELECT ok(
    NOT EXISTS (
        SELECT 1
        FROM employee_clearances ec
        JOIN deleted_employee de ON ec.employee_id = de.employee_id
    ),
    'employees cascade deletion on employee_clearances success.'
);