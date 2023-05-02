def createDepartmentTable(cur):
    # create Department table
    cur.execute('''CREATE TABLE Department(
                    depID           INTEGER UNIQUE NOT NULL,
                    depName         TEXT NOT NULL,
                    supervisorID    TEXT DEFAULT NULL,
                    description     TEXT DEFAULT '',
                    PRIMARY KEY (depID)
                    );''')
    print('Department table created\n')


def dropDepartmentTable(cur):
    # drop Department table from database if it exists
    try:
        cur.execute('DROP TABLE Department')

        print('Department table dropped\n')

    except:
        print('Department table does not exist\n')


def createDepartment_ftsTable(cur):
    cur.execute('''CREATE VIRTUAL TABLE Department_fts USING fts5(
                    depID,
                    depName,
                    supervisorID,
                    description,
                    tokenize="porter"  
                )''')
    print('Department_fts table created\n')


def dropDepartment_ftsTable(cur):
    # drop Department_fts table from database if it exists
    try:
        cur.execute('''DROP TABLE Department_fts''')

        print('Department_fts table dropped\n')

    except:
        print('Department_fts table does not exist\n')


def createDepartmentTriggers(cur):
    cur.execute('''CREATE TRIGGER department_fts_insert AFTER INSERT ON Department
                    BEGIN
                        INSERT INTO Department_fts (depID, depName, supervisorID, description)
                        VALUES (new.depID, new.depName, new.supervisorID, new.description);
                    END;''')

    cur.execute('''CREATE TRIGGER department_fts_delete AFTER DELETE ON Department
                    BEGIN
                        DELETE FROM Department_fts 
                        WHERE depID = old.depID;
                    END;''')

    cur.execute('''CREATE TRIGGER department_fts_update AFTER UPDATE ON Department
                    BEGIN
                        UPDATE Department_fts
                        SET depID = new.depID, 
                            depName = new.depName, 
                            supervisorID = new.supervisorID, 
                            description = new.description
                        WHERE depID = old.depID;
                    END;''')
