import sqlite3
from utils.variables import db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def searchEmployee(query):
    con = None
    results = None
    try:
        con = sqlite3.connect(db)
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute('''SELECT empID as empID, 
                        firstName as firstName, 
                        lastName as lastName,
                        designation as designation,
                        summary as summary
                        FROM Employee_fts(?)
                        ORDER BY rank;''', (query + '*',))
        results = cur.fetchall()

    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return results
