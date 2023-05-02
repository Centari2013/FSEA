def createSearchResultsTable(cur):
    cur.execute('''CREATE TABLE search_results(
                            type        TEXT,
                            id          TEXT,
                            firstName   TEXT,
                            lastName    TEXT,
                            description TEXT,
                            rank        INTEGER
                            );''')
    print('search_results table created')


def dropSearchResultsTable(cur):
    # drop search_results table from database if it exists
    try:
        cur.execute('''DROP TABLE search_results''')

        print('search_results table dropped\n')

    except:
        print('search_results table does not exist\n')
