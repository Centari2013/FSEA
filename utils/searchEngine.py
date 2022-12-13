import sqlite3
from utils.variables import db


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def search(query):
    con = None
    results = None
    try:
        con = sqlite3.connect(db)
        con.row_factory = dict_factory
        cur = con.cursor()
        results = [None, None, None]

        cur.execute('''CREATE TEMPORARY TABLE search_results(
                        type        TEXT,
                        id          TEXT,
                        firstName   TEXT,
                        lastName    TEXT,
                        description TEXT,
                        rank        INTEGER
                        );''')

        cur.execute('''INSERT INTO search_results (type, id, firstName, lastName, description, rank)
                        SELECT 'D', depID, NULL, depName, description, bm25(Department_fts)
                        FROM Department_fts
                        WHERE Department_fts MATCH ?
                        UNION ALL
                        SELECT 'E', empID, firstName, lastName, summary, bm25(Employee_fts)
                        FROM Employee_fts
                        WHERE Employee_fts MATCH ?
                        UNION ALL
                        SELECT 'S', specimenID, NULL, name, description, bm25(Specimen_fts)
                        FROM Specimen_fts 
                        WHERE Specimen_fts MATCH ?
                        UNION ALL
                        SELECT 'O', originID, NULL, name, description, bm25(Origin_fts)
                        FROM Origin_fts
                        WHERE Origin_fts MATCH ?
                        UNION ALL
                        SELECT 'M', missionID, NULL, name, description, bm25(Mission_fts)
                        FROM Mission_fts
                        WHERE Mission_fts MATCH ?
                        ''', (query + '*', query + '*', query + '*', query + '*', query + '*'))

        cur.execute('''SELECT type,
                        id, 
                        firstName, 
                        lastName,
                        description
                        FROM search_results
                        ORDER BY rank;''')

        results[0] = cur.fetchall()

        cur.execute('''SELECT *
                        FROM search_results
                        ORDER BY lastName;''')
        results[1] = cur.fetchall()

        cur.execute('''SELECT type,
                        id, 
                        firstName, 
                        lastName,
                        description
                        FROM search_results
                        ORDER BY lastName DESC;''')
        results[2] = cur.fetchall()

    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return results
