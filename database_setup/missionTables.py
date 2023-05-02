def createMissionTable(cur):
    cur.execute('''CREATE TABLE Mission(
                    missionID       TEXT NOT NULL UNIQUE,
                    name            TEXT NOT NULL,
                    originID        TEXT DEFAULT 'ORIGIN-PENDING',
                    startDate       TEXT DEFAULT NULL,
                    endDate         TEXT DEFAULT NULL,
                    commanderID       TEXT DEFAULT NULL,
                    supervisorID    TEXT DEFAULT NULL,
                    description     TEXT NOT NULL,
                    PRIMARY KEY (missionID),
                    FOREIGN KEY (commanderID) REFERENCES Employee(empID),
                    FOREIGN KEY (supervisorID) REFERENCES Employee(empID)
                    );''')
    print('Mission table created\n')


def dropMissionTable(cur):
    # drop Mission table from database if it exists
    try:
        cur.execute('''DROP TABLE Mission''')

        print('Mission table dropped\n')

    except:
        print('Mission table does not exist\n')


def createMission_ftsTable(cur):
    cur.execute('''CREATE VIRTUAL TABLE Mission_fts USING fts5(
                    missionID,
                    name,
                    originID,
                    startDate UNINDEXED,
                    endDate UNINDEXED,
                    commanderID,
                    supervisorID,
                    description,
                    tokenize="porter"  
                )''')
    print('Mission_fts table created\n')


def dropMission_ftsTable(cur):
    # drop Mission_fts table from database if it exists
    try:
        cur.execute('''DROP TABLE Mission_fts''')

        print('Mission_fts table dropped\n')

    except:
        print('Mission_fts table does not exist\n')


def createMissionTriggers(cur):
    cur.execute('''CREATE TRIGGER mission_fts_insert AFTER INSERT ON Mission
                    BEGIN
                        INSERT INTO Mission_fts (missionID, name, originID, startDate, endDate, commanderID, supervisorID, description)
                        VALUES (new.missionID, new.name, new.originID, new.startDate, new.endDate, new.commanderID, new.supervisorID, new.description);
                    END;''')

    cur.execute('''CREATE TRIGGER mission_fts_delete AFTER DELETE ON Mission
                    BEGIN
                        DELETE FROM Mission_fts
                        WHERE missionID = old.missionID;
                    END;''')

    cur.execute('''CREATE TRIGGER mission_fts_update AFTER UPDATE ON Mission
                    BEGIN
                        UPDATE Mission_fts
                        SET missionID = new.missionID,
                            name = new.name,
                            originID = new.originID,
                            startDate = new.startDate,
                            endDate = new.endDate, 
                            commanderID = new.commanderID,
                            supervisorID = new.supervisorID,
                            description = new.description
                        WHERE missionID = old.missionID;
                    END;''')
