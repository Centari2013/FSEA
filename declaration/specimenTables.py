from utils.dbVariables import bloodtypes, sex


def createSpecimenTable(cur):
    cur.execute('''CREATE TABLE Specimen(
                    specimenID              TEXT NOT NULL UNIQUE,
                    name                    TEXT NOT NULL,
                    origin                  TEXT DEFAULT NULL,
                    missionID               TEXT DEFAULT NULL,
                    threatLevel             REAL DEFAULT NULL,
                    acquisitionDate         TEXT NOT NULL,
                    notes                   TEXT DEFAULT NULL,
                    description             TEXT DEFAULT '',
                   PRIMARY KEY (specimenID),
                   CONSTRAINT originID FOREIGN KEY (origin) REFERENCES Origin(originID) ON DELETE CASCADE,
                   CONSTRAINT missionID FOREIGN KEY (missionID) REFERENCES Mission(missionID) ON DELETE CASCADE
                   );''')
    print('Specimen table created\n')


def dropSpecimenTable(cur):
    # drop Specimen table from database if it exists
    try:
        cur.execute('''DROP TABLE Specimen''')

        print('Specimen table dropped\n')

    except:
        print('Specimen table does not exist\n')


def createSpecimenMedicalTable(cur):
    cur.execute('''CREATE TABLE SpecimenMedical(
                    specimenID  TEXT NOT NULL,
                    bloodtype   TEXT CHECK(bloodtype IN {}) DEFAULT NULL,
                    sex         TEXT CHECK(sex IN {}) DEFAULT NULL,
                    kilograms   REAL DEFAULT NULL,
                    notes       TEXT DEFAULT NULL,
                    PRIMARY KEY (specimenID),
                    CONSTRAINT specimenID FOREIGN KEY (specimenID) REFERENCES Specimen(specimenID) ON DELETE CASCADE
                    );'''.format(bloodtypes, sex))
    print('SpecimenMedical table created\n')


def dropSpecimenMedicalTable(cur):
    # drop SpecimenMedical table from database if it exists
    try:
        cur.execute('''DROP TABLE SpecimenMedical''')

        print('SpecimenMedical table dropped\n')

    except:
        print('SpecimenMedical table does not exist\n')


def createSpecimen_ftsTable(cur):
    cur.execute('''CREATE VIRTUAL TABLE Specimen_fts USING fts5(
                    specimenID, 
                    name,
                    origin,
                    missionID, 
                    threatLevel,
                    acquisitionDate,
                    notes,
                    description,
                    tokenize="porter"  
                )''')
    print('Specimen_fts table created\n')


def dropSpecimen_ftsTable(cur):
    # drop Specimen_fts table from database if it exists
    try:
        cur.execute('''DROP TABLE Specimen_fts''')

        print('Specimen_fts table dropped\n')

    except:
        print('Specimen_fts table does not exist\n')


def createSpecimenTriggers(cur):
    cur.execute('''CREATE TRIGGER specimen_inserts AFTER INSERT ON Specimen
                    BEGIN
                        INSERT INTO Specimen_fts (specimenID, name, origin, missionID, threatLevel, acquisitionDate, notes, description)
                        VALUES (new.specimenID, new.name, new.origin, new.missionID, new.threatLevel, new.acquisitionDate, new.notes, new.description);
                        INSERT INTO SpecimenMedical (specimenID)
                        VALUES (new.specimenID);
                        INSERT INTO SpecimenContainmentStatus (specimenID)
                        VALUES (new.specimenID);
                    END;''')

    cur.execute('''CREATE TRIGGER specimen_fts_delete AFTER DELETE ON Specimen
                    BEGIN
                        DELETE FROM Specimen_fts
                        WHERE specimenID = old.specimenID;
                    END;''')

    cur.execute('''CREATE TRIGGER specimen_fts_update AFTER UPDATE ON Specimen
                    BEGIN
                        UPDATE Specimen_fts
                        SET specimenID = new.specimenID,
                            name = new.name,
                            origin = new.origin,
                            missionID = new.missionID,
                            threatLevel = new.threatLevel,
                            acquisitionDate = new.acquisitionDate,
                            notes = new.notes,
                            description = new.description
                        WHERE specimenID = old.specimenID;
                        UPDATE SpecimenMedical
                        SET specimenID = new.specimenID
                        WHERE specimenID = old.specimenID;
                    END;''')
