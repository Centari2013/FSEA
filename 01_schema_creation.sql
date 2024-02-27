CREATE TABLE clearances (
    clearanceID SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE containmentStatuses (
    containmentStatusID SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE departments (
    departmentID SERIAL PRIMARY KEY,
    departmentName TEXT NOT NULL,
    supervisorID VARCHAR(8), -- Assuming employeeID types for consistency
    description TEXT DEFAULT NULL
);

CREATE TABLE designations (
    designationID SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    abbreviation VARCHAR(10) NOT NULL
);

CREATE TABLE employees (
    employeeID VARCHAR(8) PRIMARY KEY, -- Employee IDs are formatted as 'EXXXXXXX'
    departmentID INTEGER NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE DEFAULT NULL,
    summary TEXT DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (departmentID) REFERENCES departments(departmentID)
);

CREATE TABLE employeeClearances (
    employeeID VARCHAR(8),
    clearanceID INTEGER,
    PRIMARY KEY (employeeID, clearanceID),
    FOREIGN KEY (employeeID) REFERENCES employees(employeeID) ON DELETE CASCADE,
    FOREIGN KEY (clearanceID) REFERENCES clearances(clearanceID) ON DELETE CASCADE
);

CREATE TABLE employeeDesignations (
    employeeID VARCHAR(8),
    designationID INTEGER NOT NULL,
    PRIMARY KEY (employeeID, designationID),
    FOREIGN KEY (employeeID) REFERENCES employees(employeeID),
    FOREIGN KEY (designationID) REFERENCES designations(designationID)
);

CREATE TABLE employeeMedicalRecords (
    employeeID VARCHAR(8) PRIMARY KEY,
    dob DATE,
    bloodtype VARCHAR(10) DEFAULT NULL CHECK (bloodtype IN ('A+', 'O+', 'B+', 'AB+', 'A-', 'O-', 'B-', 'AB-', 'V-', 'V+', 'BF', 'undefined')),
    sex VARCHAR(10) DEFAULT NULL CHECK (sex IN ('m', 'f', 'inter', 'unknown', 'undefined')),
    kilograms REAL CHECK(kilograms > 0),
    height_cm REAL CHECK (height_cm > 0),
    notes TEXT DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (employeeID) REFERENCES employees(employeeID) ON DELETE CASCADE
);

CREATE TABLE missions (
    missionID VARCHAR(8) PRIMARY KEY, -- Mission IDs are formatted as 'MXXXXXXX'
    name TEXT NOT NULL DEFAULT 'NAME-PENDING',
    startDate DATE,
    endDate DATE,
    commanderID VARCHAR(8),
    supervisorID VARCHAR(8),
    description TEXT NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (commanderID) REFERENCES employees(employeeID),
    FOREIGN KEY (supervisorID) REFERENCES employees(employeeID) 
);

CREATE TABLE origins (
    originID VARCHAR(8) PRIMARY KEY, -- Origin IDs are formatted as 'OXXXXXXX'
    name TEXT NOT NULL,
    discoveryDate DATE NOT NULL,
    description TEXT NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL
);

CREATE TABLE missionOrigins(
    missionID VARCHAR(8) NOT NULL,
    originID VARCHAR(8) NOT NULL,
    PRIMARY KEY (missionID, originID),
    FOREIGN KEY (originID) REFERENCES origins(originID),
    FOREIGN KEY (missionID) REFERENCES missions(missionID) 
);

CREATE TABLE specimens (
    specimenID VARCHAR(8) PRIMARY KEY, -- SpecimenIDs are formatted as 'SXXXXXXX'
    name TEXT NOT NULL,
    originID VARCHAR(8),
    missionID VARCHAR(8),
    threatLevel REAL CHECK (threatLevel >= 0 AND threatLevel <= 10),
    acquisitionDate DATE NOT NULL,
    notes TEXT DEFAULT NULL,
    description TEXT DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (originID) REFERENCES origins(originID) ON DELETE CASCADE,
    FOREIGN KEY (missionID) REFERENCES missions(missionID) ON DELETE CASCADE
);

CREATE TABLE specimenContainmentStatuses (
    specimenID VARCHAR(8) NOT NULL,
    containmentStatusID INTEGER,
    PRIMARY KEY (specimenID, containmentStatusID),
    FOREIGN KEY (specimenID) REFERENCES specimens(specimenID) ON DELETE CASCADE,
    FOREIGN KEY (containmentStatusID) REFERENCES containmentStatuses(containmentStatusID) ON DELETE CASCADE
);

CREATE TABLE specimenMedicalRecords (
    specimenID VARCHAR(8) PRIMARY KEY ,
    bloodtype VARCHAR(10) DEFAULT NULL,
    sex VARCHAR(10) DEFAULT NULL,
    kilograms REAL CHECK(kilograms > 0),
    notes TEXT DEFAULT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (specimenID) REFERENCES specimens(specimenID) ON DELETE CASCADE
);

CREATE TABLE specimenMissions (
    specimenID VARCHAR(8) NOT NULL,
    missionID VARCHAR(8) NOT NULL,
    involvementSummary TEXT,
    PRIMARY KEY (specimenID, missionID),
    FOREIGN KEY (specimenID) REFERENCES specimens(specimenID) ON DELETE CASCADE,
    FOREIGN KEY (missionID) REFERENCES missions(missionID) ON DELETE CASCADE
);

CREATE TABLE credentials (
    employeeID VARCHAR(8) PRIMARY KEY ,
    username DEFAULT NULL,
    password DEFAULT NULL,
    loginAttempts INTEGER DEFAULT 0,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    FOREIGN KEY (employeeID) REFERENCES employees(employeeID) ON DELETE CASCADE
);

-- maybe add onboarding table for tracking user onboarding tasks

CREATE TABLE departmentMissions (
    departmentID INTEGER NOT NULL,
    missionID VARCHAR(8) NOT NULL,
    PRIMARY KEY (departmentID, missionID),
    FOREIGN KEY (departmentID) REFERENCES departments(departmentID) ON DELETE CASCADE,
    FOREIGN KEY (missionID) REFERENCES missions(missionID) ON DELETE CASCADE
);

CREATE TABLE employeeMissions (
    employeeID VARCHAR(8) NOT NULL,
    missionID VARCHAR(8) NOT NULL,
    involvementSummary TEXT DEFAULT NULL,
    PRIMARY KEY (employeeID, missionID),
    FOREIGN KEY (employeeID) REFERENCES employees(employeeID) ON DELETE CASCADE,
    FOREIGN KEY (missionID) REFERENCES missions(missionID) ON DELETE CASCADE
);

CREATE TABLE researcherSpecimens (
    employeeID VARCHAR(8) NOT NULL,
    specimenID VARCHAR(8) NOT NULL,
    PRIMARY KEY (employeeID, specimenID),
    FOREIGN KEY (employeeID) REFERENCES employees(employeeID) ON DELETE CASCADE,
    FOREIGN KEY (specimenID) REFERENCES specimens(specimenID) ON DELETE CASCADE
);
