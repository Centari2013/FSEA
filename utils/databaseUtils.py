import sqlite3
from utils.filePaths import DB_PATH
from utils.authUtils import generateEID, generateUsername, generatePWD, generateOID, generateMID, generateSID
from abc import ABC, abstractmethod
import traceback

'''''''''''''''''''''ALTER DATABASE'''''''''''''''''''''


class DatabaseManager(ABC):
    @staticmethod
    @abstractmethod
    def add(**kwargs):
        pass

    @staticmethod
    @abstractmethod
    def update(**kwargs):
        pass

    @staticmethod
    @abstractmethod
    def delete(**kwargs):
        pass

    @staticmethod
    @abstractmethod
    def get(**kwargs):
        pass

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def _execute(query, params=None):
        con = None
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON;")
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            con.commit()
            return True, cur.lastrowid
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            if con is not None:
                con.close()
        return False

    @staticmethod
    def _execute_with_return(query, params=None):
        con = None
        try:
            con = sqlite3.connect(DB_PATH)
            con.row_factory = DatabaseManager._dict_factory
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON;")
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            con.commit()
            result = cur.fetchall()
            return result if result else None
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            if con is not None:
                con.close()
        return None

    @staticmethod
    def _get_id_from_row(rowid, table_name, *column_names):
        column_names_str = ', '.join(column_names)
        query = f'SELECT {column_names_str} FROM {table_name} WHERE rowid = ?;'
        con = None
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON;")
            cur.execute(query, (rowid,))
            result = cur.fetchone()
            return result if result else None
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            if con is not None:
                con.close()
        return None


class manageContainmentStatus(DatabaseManager):
    @staticmethod
    def add(name, desc):
        success, rowid = DatabaseManager._execute('INSERT INTO ContainmentStatus(name, description) VALUES(?,?);',
                                                  (name, desc))
        return DatabaseManager._get_id_from_row(rowid, 'ContainmentStatus', 'containmentStatusID') if success else None

    @staticmethod
    def update(containmentStatusID, name=None, desc=None):
        args = [[name, 'name'], [desc, 'desc']]
        success = True
        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute(
                    f'''UPDATE ContainmentStatus SET {a[1]} = ? WHERE containmentStatusID = ?''',
                    (a[0], containmentStatusID))
                if not success:
                    break

        return success

    @staticmethod
    def delete(containmentStatusID):
        success, rowid = DatabaseManager._execute('DELETE FROM ContainmentStatus WHERE containmentStatusID = ?',
                                                  (containmentStatusID,))
        return success

    @staticmethod
    def get(containmentStatusID):
        return DatabaseManager._execute_with_return('SELECT * FROM ContainmentStatus WHERE containmentStatusID = ?', (containmentStatusID,))


class manageClearance(DatabaseManager):
    @staticmethod
    def add(name, desc):
        success, rowid = DatabaseManager._execute('INSERT INTO Clearance(name, description) VALUES(?,?);', (name, desc))
        return DatabaseManager._get_id_from_row(rowid, 'Clearance', 'clearanceID') if success else None

    @staticmethod
    def update(clearanceID, name=None, desc=None):
        success = True
        args = [[name, 'name'], [desc, 'desc']]
        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute(f'''UPDATE Clearance SET {a[1]} = ? WHERE clearanceID = ?''',
                                                          (a[0], clearanceID))
                if not success:
                    break
        return success

    @staticmethod
    def delete(clearanceID):
        success, rowid = DatabaseManager._execute('DELETE FROM Clearance WHERE clearanceID = ?', (clearanceID,))
        return success

    @staticmethod
    def get(clearanceID):
        return DatabaseManager._execute_with_return('SELECT * FROM Clearance WHERE clearanceID = ?', (clearanceID,))


class manageEmployeeClearance(DatabaseManager):
    @staticmethod
    def add(empID, clearanceID):
        success, rowid = DatabaseManager._execute('INSERT INTO EmployeeClearance(empID, clearanceID) VALUES(?,?);',
                                                  (empID, clearanceID))
        return DatabaseManager._get_id_from_row(rowid, 'EmployeeClearance', 'empID', 'clearanceID') if success else None

    @staticmethod
    def update(empID, oldClearanceID, newClearanceID):
        success, rowid = DatabaseManager._execute(
            f'''UPDATE EmployeeClearance SET clearanceID = ? WHERE empID = ? AND clearanceID = ?''',
            (empID, oldClearanceID, newClearanceID))
        return success

    @staticmethod
    def delete(empID, clearanceID):
        success, rowid = DatabaseManager._execute('DELETE FROM EmployeeClearance WHERE empID = ? AND clearanceID = ?',
                                                  (empID, clearanceID,))
        return success

    @staticmethod
    def get(empID):
        return DatabaseManager._execute_with_return('SELECT * FROM EmployeeClearance where empID = ?', (empID,))

    @staticmethod
    def getByClearance(clearanceID):
        return DatabaseManager._execute_with_return('SELECT * FROM EmployeeClearance where clearanceID = ?', (clearanceID,))


class manageDesignation(DatabaseManager):
    @staticmethod
    def add(name, abbreviation):
        success, rowid = DatabaseManager._execute('INSERT INTO Designation(name, abbreviation) VALUES(?,?);',
                                                  (name, abbreviation))
        return DatabaseManager._get_id_from_row(rowid, 'Designation', 'designationID') if success else None

    @staticmethod
    def update(designationID, name=None, abbreviation=None):
        success = True
        args = [[name, 'name'], [abbreviation, 'abbreviation']]
        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute(
                    f'''UPDATE Designation SET {a[1]} = ? WHERE designationID = ?''', (a[0], designationID))
                if not success:
                    break
        return success

    @staticmethod
    def delete(designationID):
        success, rowid = DatabaseManager._execute('DELETE FROM Designation WHERE designationID = ?', (designationID,))
        return success

    @staticmethod
    def get(designationID):
        return DatabaseManager._execute_with_return('SELECT * FROM Designation WHERE designationID = ?', (designationID,))


class manageDepartment(DatabaseManager):

    @staticmethod
    def add(name, supervisorID=None, desc=None):
        success, rowid = DatabaseManager._execute('INSERT INTO Department(depName) VALUES(?);', (name,))
        return DatabaseManager._get_id_from_row(rowid, 'Department', ) if success else None

    @staticmethod
    def update(depID, name=None, supervisorID=None, desc=None):
        success = True
        args = [[name, 'depName'], [supervisorID, 'supervisorID'], [desc, 'description']]
        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute(f'''UPDATE Department SET {a[1]} = ? WHERE depID = ?''',
                                                          (a[0], depID))
                if not success:
                    break
        return success

    @staticmethod
    def delete(depID):
        success, rowid = DatabaseManager._execute('DELETE FROM Department WHERE depID = ?', (depID,))
        return success

    @staticmethod
    def get(depID):
        return DatabaseManager._execute_with_return('SELECT * FROM Department WHERE depID = ?',(depID,))


class manageEmployee(DatabaseManager):
    @staticmethod
    def add(firstName, lastName, dep, startDate, summary=None):
        ID = generateEID()
        result = DatabaseManager._execute_with_return('SELECT empID FROM Employee WHERE empID = ?', (ID,))

        while result is not None:
            ID = generateEID()
            result = DatabaseManager._execute_with_return('SELECT empID FROM Employee WHERE empID = ?', (ID,))

        success, rowid = DatabaseManager._execute('''INSERT INTO Employee(empDep, empID,firstName, lastName, startDate) 
                                VALUES(?,?,?,?,?)''', (dep, ID, firstName, lastName, startDate))

        manageEmployee.update(ID, summary=summary)
        manageEmployee.updateCredentials(ID, username=generateUsername(firstName, lastName, dep), pwd=generatePWD())

        return ID if success else None

    @staticmethod
    def update(empID, dep=None, role=None, firstName=None, lastName=None, startDate=None, endDate=None,
               summary=None):
        success = True
        args = [[dep, 'empDep'], [role, 'designation'], [firstName, 'firstName'],
                [lastName, 'lastName'], [startDate, 'startDate'], [endDate, 'endDate'], [summary, 'summary']]

        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute('''UPDATE Employee
                                        SET {} = ?
                                        WHERE empID = ?'''.format(a[1]), (a[0], empID))
                if not success:
                    break
        return success

    @staticmethod
    def delete(empID):
        success, rowid = DatabaseManager._execute('DELETE FROM Employee WHERE empID = ?', (empID,))
        return success

    @staticmethod
    def get(empID):
        return DatabaseManager._execute_with_return('SELECT * FROM Employee WHERE empID = ?',(empID,))

    @staticmethod
    def getMedical(empID):
        return DatabaseManager._execute_with_return('SELECT * FROM EmployeeMedical WHERE empID = ?', (empID,))

    @staticmethod
    def updateCredentials(empID, username=None, pwd=None):
        success = True
        args = [[username, 'username'], [pwd, 'password']]

        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute('''UPDATE Credentials
                                                SET {} = ?
                                                WHERE empID = ?'''.format(a[1]), (a[0], empID))
                if not success:
                    break
        return success

    @staticmethod
    def updateEmployeeMedical(empID, dob=None, bloodtype=None, sex=None, kg=None, height=None, notes=None):
        args = [[dob, 'dob'], [bloodtype, 'bloodtype'], [sex, 'sex'],
                [kg, 'kilograms'], [height, 'height'], [notes, 'notes']]
        success = True
        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute(
                    'UPDATE EmployeeMedical SET {} = ? WHERE empID = ?'.format(a[1]), (a[0], empID))
                if not success:
                    break

        return success


class manageEmployeeDesignation(DatabaseManager):
    @staticmethod
    def add(empID, designationID):
        success, rowid = DatabaseManager._execute('''INSERT INTO EmployeeDesignation(empID, designationID) 
                        VALUES(?,?)''', (empID, designationID))
        return success

    @staticmethod
    def update(empID, oldDesignationID, newDesignationID):
        success, rowid = DatabaseManager._execute(
            'UPDATE EmployeeDesignation SET designationID = ? WHERE empID = ? AND designationID = ?',
            (newDesignationID, empID, oldDesignationID))
        return success

    @staticmethod
    def delete(empID, designationID):
        success, rowid = DatabaseManager._execute(
            'DELETE FROM EmployeeDesignation WHERE empID = ? AND designationID = ?', (empID, designationID))
        return success

    @staticmethod
    def get(empID):
        return DatabaseManager._execute_with_return('SELECT * FROM EmployeeDesignation WHERE empID = ?', (empID,))

    @staticmethod
    def getByDesignation(designationID):
        return DatabaseManager._execute_with_return('SELECT * FROM EmployeeDesignation WHERE designationID = ?', (designationID,))


class manageOrigin(DatabaseManager):
    @staticmethod
    def add(name, discoveryDate, desc):
        ID = generateOID()
        result = DatabaseManager._execute_with_return('SELECT originID FROM Origin WHERE originID = ?', (ID,))

        while result is not None:
            ID = generateOID()
            result = DatabaseManager._execute_with_return('SELECT originID FROM Origin WHERE originID = ?', (ID,))

        success, rowid = DatabaseManager._execute('INSERT INTO Origin(originID, name, description, discoveryDate) '
                                                  'VALUES (?,?,?,?)',
                                                  (ID, name, desc, discoveryDate))
        return ID if success else None




def updateOrigin(ID, name=None, desc=None, discoveryDate=None):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[name, 'name'], [discoveryDate, 'discoveryDate'], [desc, 'description']]

        for a in args:
            if a[0] is not None:
                cur.execute(f'UPDATE Origin SET {a[1]} = ? WHERE originID = ?', (a[0], ID))

        con.commit()
        success = True
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()
        return success


def deleteOrigin(originID):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM Origin WHERE originID = ?', (originID,))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()
        return success


def addMission(name, desc, originID=None, startDate=None, endDate=None, captainID=None, supervisorID=None):
    ID = None
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        ID = generateMID()

        cur.execute('SELECT missionID FROM Mission WHERE missionID = ?', (ID,))
        r = cur.fetchone()

        while r is not None:
            ID = generateMID()
            cur.execute('SELECT missionID FROM Mission WHERE missionID = ?', (ID,))
            r = cur.fetchone()

        cur.execute('INSERT INTO Mission(missionID, name, description) VALUES (?,?,?)', (ID, name, desc))
        con.commit()

        updateMission(ID, name, originID, startDate, endDate, captainID, supervisorID)
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return ID


def updateMission(missionID, name=None, desc=None, originID=None, startDate=None, endDate=None, captainID=None,
                  supervisorID=None):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[name, 'name'], [desc, 'description'], [originID, 'originID'], [startDate, 'startDate'],
                [endDate, 'endDate'], [captainID, 'captainID'], [supervisorID, 'supervisorID']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE Mission SET {} = ? WHERE missionID = ?'.format(a[1]), (a[0], missionID))

        con.commit()
        success = True
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()
        return success


def deleteMission(missionID):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM Mission WHERE missionID = ?', (missionID,))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()
        return success


def addSpecimen(name, acquisitionDate, originID=None, missionID=None, threatLevel=None, notes=None, description=None):
    con = None
    ID = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        ID = generateSID()
        # check for repeat ID
        cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', (ID,))
        r = cur.fetchone()

        while r is not None:
            ID = generateSID()
            cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', (ID,))
            r = cur.fetchone()

        cur.execute('INSERT INTO Specimen(specimenID, name, acquisitionDate) VALUES (?,?,?)',
                    (ID, name, acquisitionDate))
        con.commit()

        updateSpecimen(ID, originID=originID, missionID=missionID, threatLevel=threatLevel, notes=notes,
                       description=description)

    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        if con is not None:
            con.close()
        return ID


def updateSpecimen(ID, name=None, acquisitionDate=None, originID=None, missionID=None, threatLevel=None, notes=None,
                   description=None):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[name, 'name'], [acquisitionDate, 'acquisitionDate'], [originID, 'originID'],
                [missionID, 'missionID'], [threatLevel, 'threatLevel'], [notes, 'notes'], [description, 'description']]

        for a in args:
            if a[0] is not None:
                cur.execute(f'UPDATE Specimen SET {a[1]} = ? WHERE specimenID = ?', (a[0], ID))

        con.commit()
        success = True
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        if con is not None:
            con.close()
        return success


def deleteSpecimen(specimenID):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM Specimen WHERE specimenID = ?', (specimenID,))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return False


def addResearcherSpecimen(empID, specimenID):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('INSERT INTO ResearcherSpecimen(empID, specimenID) VALUES(?,?)', (empID, specimenID))
        con.commit()
        success = True
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()
        return success


def updateSpecimenSupervisor(empID, specimenID, newEmployeeID):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('''UPDATE ResearcherSpecimen
                        SET empID = ?
                        WHERE empID = ? AND specimenID = ?''', (newEmployeeID, empID, specimenID))
        con.commit()
        success = True
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()
        return success


def updateSupervisorSpecimen(empID, specimenID, newSpecimenID):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('''UPDATE ResearcherSpecimen
                            SET specimenID = ?
                            WHERE empID = ? AND specimenID = ?''', (newSpecimenID, empID, specimenID))
        con.commit()
        success = True
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()
        return success


def deleteResearcherSpecimen(empID, specimenID):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM ResearcherSpecimen WHERE empID = ? AND specimenID = ?', (empID, specimenID))
        con.commit()
        success = True
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return success


def updateSpecimenMedical(ID, name=None, acquisitionDate=None, bloodtype=None, sex=None, kg=None, notes=None):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[name, 'name'], [acquisitionDate, 'acquisitionDate'], [bloodtype, 'bloodtype'], [sex, 'sex'],
                [kg, 'kilograms'], [notes, 'notes']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE SpecimenMedical SET {} = ? WHERE specimenID = ?'.format(a[1]), (a[0], ID))

        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success
