import sqlite3
import string
import logging
from utils.filePaths import DB_PATH
from nltk.corpus import stopwords


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d





class searchEngine:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='searchEngine.log', encoding='utf-8', level=logging.ERROR)
        try:
            instance.con = sqlite3.connect(DB_PATH)
            instance.con.row_factory = _dict_factory
            instance.cur = instance.con.cursor()

        except Exception as e:
            logging.error(e)
            return None

        finally:
            return instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()


    def _cleanQuery(self, query):
        query = str(query).translate(
            str.maketrans('', '', string.punctuation))  # remove punctuation to avoid syntax error
        query = query.split()
        query = [w for w in query if not w in stopwords.words('english')]  # remove stopwords
        q_length = len(query)
        cleanQ = ''.join([(query[i] + '* AND ') if i != (q_length - 1) else (query[i] + '*') for i in range(q_length)])

        return cleanQ


    def search(self, query):

        results = None
        try:
            results = [None, None, None]

            q = self._cleanQuery(query)

            self.cur.execute('''DELETE FROM search_results;''')

            self.cur.execute('''INSERT INTO search_results (type, id, firstName, lastName, description, rank)
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
                            ''', (q, q, q, q, q))

            self.cur.execute('''SELECT type,
                            id,
                            firstName,
                            lastName,
                            description
                            FROM search_results
                            ORDER BY rank;''')

            results[0] = self.cur.fetchall()

            self.cur.execute('''SELECT *
                            FROM search_results
                            ORDER BY lastName;''')
            results[1] = self.cur.fetchall()

            self.cur.execute('''SELECT type,
                            id,
                            firstName,
                            lastName,
                            description
                            FROM search_results
                            ORDER BY lastName DESC;''')
            results[2] = self.cur.fetchall()



        except Exception as e:
            self.logger.error(e)
            return False

        finally:
            return results
