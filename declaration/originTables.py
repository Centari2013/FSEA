def createOriginTable(cur):
    # create Origin table
    cur.execute('''CREATE TABLE Origin(
                    originID    TEXT NOT NULL UNIQUE,
                    name        TEXT NOT NULL,
                    discoveryDate   TEXT NOT NULL,
                    description TEXT NOT NULL,
                    PRIMARY KEY (originID)
                    );''')
    print('Origin table created\n')


def dropOriginTable(cur):
    # drop Origin table from database if it exists
    try:
        cur.execute('''DROP TABLE Origin''')

        print('Origin table dropped\n')

    except:
        print('Origin table does not exist\n')


def createOrigin_ftsTable(cur):
    cur.execute('''CREATE VIRTUAL TABLE Origin_fts USING fts5(
                    originID,
                    name,
                    discoveryDate,
                    description,
                    tokenize="porter"  
                )''')
    print('Origin_fts table created\n')


def dropOrigin_ftsTable(cur):
    # drop Origin_fts table from database if it exists
    try:
        cur.execute('''DROP TABLE Origin_fts''')

        print('Origin_fts table dropped\n')

    except:
        print('Origin_fts table does not exist\n')


def createOriginTriggers(cur):
    cur.execute('''CREATE TRIGGER origin_fts_insert AFTER INSERT ON Origin
                    BEGIN
                        INSERT INTO Origin_fts (originID, name, discoveryDate, description)
                        VALUES (new.originID, new.name, new.discoveryDate, new.description);
                    END;''')

    cur.execute('''CREATE TRIGGER origin_fts_delete AFTER DELETE ON Origin
                    BEGIN
                        DELETE FROM Origin_fts 
                        WHERE originID = old.originID;
                    END;''')

    cur.execute('''CREATE TRIGGER origin_fts_update AFTER UPDATE ON Origin
                    BEGIN
                        UPDATE Origin_fts
                        SET originID = new.originID,
                            name = new.name,
                            discoveryDate = new.discoveryDate,
                            description = new.description
                        WHERE originID = old.originID;
                    END;''')
