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
            print(query)
            print(params)
            traceback.print_exc()
        finally:
            if con is not None:
                con.close()
        return False, None

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

            if len(result) == 1:
                return result[0]  # Return the dictionary directly
            elif len(result) > 1:
                return result  # Return the list of dictionaries

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
            return result[0] if result else None
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
        return DatabaseManager._execute_with_return('SELECT * FROM ContainmentStatus WHERE containmentStatusID = ?',
                                                    (containmentStatusID,))


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
        return DatabaseManager._execute_with_return('SELECT * FROM Designation WHERE designationID = ?',
                                                    (designationID,))


class manageDepartment(DatabaseManager):

    @staticmethod
    def add(name, supervisorID=None, desc=None):
        success, rowid = DatabaseManager._execute('INSERT INTO Department(depName) VALUES(?);', (name,))
        return DatabaseManager._get_id_from_row(rowid, 'Department', 'depID') if success else None

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
        return DatabaseManager._execute_with_return('SELECT * FROM Department WHERE depID = ?', (depID,))

    @staticmethod
    def addMission(depID, missionID):
        success, rowid = DatabaseManager._execute('INSERT INTO DepartmentMission (depID, missionID) VALUES '
                                                  '(?,?)', (depID, missionID))
        return success

    @staticmethod
    def updateMissionID(depID, oldMissionID, newMissionID):
        success, rowid = DatabaseManager._execute('UPDATE DepartmentMission SET missionID = ? '
                                                  'WHERE depID = ? AND missionID = ?',
                                                  (newMissionID, depID, oldMissionID))
        return success

    @staticmethod
    def deleteMissionID(depID, missionID):
        success, rowid = DatabaseManager._execute('DELETE FROM DepartmentMission WHERE depID = ? AND missionID = ?',
                                                  (depID, missionID))
        return success



class manageEmployee(DatabaseManager):
    @staticmethod
    def add(firstName, lastName, dep, startDate, summary=None):
        ID = generateEID()

        while manageEmployee._check_employee_exists(ID):
            ID = generateEID()

        success, rowid = DatabaseManager._execute('''INSERT INTO Employee(empDep, empID,firstName, lastName, startDate) 
                                VALUES(?,?,?,?,?)''', (dep, ID, firstName, lastName, startDate))

        if not success:
            return success

        success = manageEmployee.update(ID, summary=summary)

        if not success:
            return success

        success = manageEmployee.updateCredentials(ID, username=generateUsername(firstName, lastName, dep),
                                                   pwd=generatePWD())

        return ID if success else None

    @staticmethod
    def _check_employee_exists(empID):
        result = DatabaseManager._execute_with_return('SELECT empID FROM Employee WHERE empID = ?', (empID,))
        return result is not None

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
        return DatabaseManager._execute_with_return('SELECT * FROM Employee WHERE empID = ?', (empID,))

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

    @staticmethod
    def updateEmployeeClearance(empID, newClearanceID):
        success, rowid = DatabaseManager._execute(
            f'''UPDATE EmployeeClearance SET clearanceID = ? WHERE empID = ?''',
            (newClearanceID, empID))
        return success


    @staticmethod
    def getEmployeeClearance(empID):
        return DatabaseManager._execute_with_return('SELECT clearanceID FROM EmployeeClearance where empID = ?', (empID,))

    @staticmethod
    def getByClearance(clearanceID):
        return DatabaseManager._execute_with_return('SELECT * FROM EmployeeClearance where clearanceID = ?',
                                                    (clearanceID,))




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
        return DatabaseManager._execute_with_return('SELECT * FROM EmployeeDesignation WHERE designationID = ?',
                                                    (designationID,))


class manageOrigin(DatabaseManager):
    @staticmethod
    def add(name, discoveryDate, desc):
        ID = generateOID()

        while manageOrigin._check_origin_exists(ID):
            ID = generateOID()

        success, rowid = DatabaseManager._execute('INSERT INTO Origin(originID, name, description, discoveryDate) '
                                                  'VALUES (?,?,?,?)',
                                                  (ID, name, desc, discoveryDate))

        return ID if success else None

    @staticmethod
    def _check_origin_exists(originID):
        result = DatabaseManager._execute_with_return('SELECT originID FROM Origin WHERE originID = ?', (originID,))
        return result is not None

    @staticmethod
    def update(ID, name=None, desc=None, discoveryDate=None):
        success = True
        args = [[name, 'name'], [discoveryDate, 'discoveryDate'], [desc, 'description']]

        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute(f'UPDATE Origin SET {a[1]} = ? WHERE originID = ?',
                                                          (a[0], ID))
                if not success:
                    break

        return success

    @staticmethod
    def delete(originID):
        success, rowid = DatabaseManager._execute('DELETE FROM Origin WHERE originID = ?', (originID,))
        return success

    @staticmethod
    def get(originID):
        return DatabaseManager._execute_with_return('SELECT * FROM Origin WHERE originID = ?', (originID,))


class manageMission(DatabaseManager):
    @staticmethod
    def add(name, desc, startDate=None, endDate=None, commanderID=None, supervisorID=None, originID=None):
        ID = generateMID()

        while manageMission._check_mission_exists(ID):
            ID = generateMID()

        success, rowid = DatabaseManager._execute('INSERT INTO Mission(missionID, name, description) VALUES (?,?,?)',
                                                  (ID, name, desc))
        if not success:
            return success

        success = manageMission.update(ID, startDate=startDate,
                                       endDate=endDate,
                                       commanderID=commanderID,
                                       supervisorID=supervisorID,
                                       originID=originID)

        return ID if success else None

    @staticmethod
    def _check_mission_exists(missionID):
        result = DatabaseManager._execute_with_return('SELECT missionID FROM Mission WHERE missionID = ?', (missionID,))
        return result is not None

    @staticmethod
    def update(missionID, name=None, desc=None, startDate=None, endDate=None, commanderID=None,
               supervisorID=None, originID=None):
        args = [[name, 'name'], [desc, 'description'], [startDate, 'startDate'], [originID, 'originID'],
                [endDate, 'endDate'], [commanderID, 'commanderID'], [supervisorID, 'supervisorID']]

        success = True

        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute('UPDATE Mission SET {} = ? WHERE missionID = ?'.format(a[1]),
                                                          (a[0], missionID))
                if not success:
                    break

        return success

    @staticmethod
    def delete(missionID):
        success, rowid = DatabaseManager._execute('DELETE FROM Mission WHERE missionID = ?', (missionID,))
        return success

    @staticmethod
    def get(missionID):
        return DatabaseManager._execute_with_return('SELECT * FROM Mission WHERE missionID = ?', (missionID,))

    @staticmethod
    def getMissionByEmpID(empID):
        return DatabaseManager._execute_with_return('SELECT missionID FROM EmployeeMission WHERE empID = ?', (empID,))

    @staticmethod
    def getEmployeeByMissionID(missionID):
        return DatabaseManager._execute_with_return('SELECT * FROM Employee WHERE empID ='
                                                    '(SELECT empID FROM EmployeeMission WHERE missionID = ?)', (missionID,))

    @staticmethod
    def addEmployeeToMission(empID, missionID):
        success, rowid = DatabaseManager._execute('INSERT INTO EmployeeMission(empID, missionID)'
                                                  'VALUES (?,?)', (empID, missionID))
        return success

    @staticmethod
    def deleteEmployeeFromMission(empID, missionID):
        success, rowid = DatabaseManager._execute(
            'DELETE FROM EmployeeMission WHERE empID = ? AND missionID = ?'.format,
            (empID, missionID))
        return success


class manageSpecimen(DatabaseManager):
    @staticmethod
    def add(name, acquisitionDate, originID=None, missionID=None, threatLevel=None, notes=None, description=None):
        ID = generateSID()

        while manageSpecimen._check_specimen_exists(ID):
            ID = generateSID()

        success, rowid = DatabaseManager._execute(
            'INSERT INTO Specimen(specimenID, name, acquisitionDate) VALUES (?,?,?)',
            (ID, name, acquisitionDate))

        if not success:
            return success

        success = manageSpecimen.update(ID, originID=originID, missionID=missionID, threatLevel=threatLevel,
                                        notes=notes,
                                        description=description)

        return ID if success else None

    @staticmethod
    def _check_specimen_exists(specimenID):
        result = DatabaseManager._execute_with_return('SELECT specimenID FROM Specimen WHERE specimenID = ?', (specimenID,))
        return result is not None

    @staticmethod
    def update(ID, name=None, acquisitionDate=None, originID=None, missionID=None, threatLevel=None, notes=None,
               description=None):
        args = [[name, 'name'], [acquisitionDate, 'acquisitionDate'], [originID, 'originID'],
                [missionID, 'missionID'], [threatLevel, 'threatLevel'], [notes, 'notes'], [description, 'description']]
        success = True
        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute(f'UPDATE Specimen SET {a[1]} = ? WHERE specimenID = ?',
                                                          (a[0], ID))
                if not success:
                    break
        return success

    @staticmethod
    def updateSpecimenMedical(ID, bloodtype=None, sex=None, kg=None, notes=None):

        args = [[bloodtype, 'bloodtype'], [sex, 'sex'],
                [kg, 'kilograms'], [notes, 'notes']]

        success = True

        for a in args:
            if a[0] is not None:
                success, rowid = DatabaseManager._execute(
                    'UPDATE SpecimenMedical SET {} = ? WHERE specimenID = ?'.format(a[1]), (a[0], ID))
                if not success:
                    break
        return success

    @staticmethod
    def getContainmentStatus(specimenID):
        return DatabaseManager._execute_with_return('SELECT * FROM SpecimenContainmentStatus WHERE specimenID = ?', (specimenID,))

    @staticmethod
    def updateSpecimenContainmentStatus(specimenID, newContainmentStatus):
        success, rowid = DatabaseManager._execute(
            'UPDATE SpecimenContainmentStatus SET containmentStatusID = ? WHERE specimenID = ?''', (newContainmentStatus, specimenID))
        return success


    @staticmethod
    def delete(specimenID):
        success, rowid = DatabaseManager._execute('DELETE FROM Specimen WHERE specimenID = ?', (specimenID,))
        return success

    @staticmethod
    def get(specimenID):
        return DatabaseManager._execute_with_return('SELECT * FROM Specimen WHERE specimenID = ?', (specimenID,))


class manageResearcherSpecimen(DatabaseManager):
    @staticmethod
    def add(empID, specimenID):
        success, rowid = DatabaseManager._execute('INSERT INTO ResearcherSpecimen(empID, specimenID) VALUES(?,?)',
                                                  (empID, specimenID))
        return success

    @staticmethod
    def update(oldEmpID, specimenID, newEmployeeID):
        success, rowid = DatabaseManager._execute('''UPDATE ResearcherSpecimen
                        SET empID = ?
                        WHERE empID = ? AND specimenID = ?''', (newEmployeeID, oldEmpID, specimenID))
        return success

    @staticmethod
    def delete(empID, specimenID):
        success, rowid = DatabaseManager._execute('DELETE FROM ResearcherSpecimen WHERE empID = ? AND specimenID = ?',
                                                  (empID, specimenID))
        return success

    @staticmethod
    def get(empID):
        return DatabaseManager._execute_with_return('SELECT * FROM ResearcherSpecimen WHERE empID = ?', (empID,))

    @staticmethod
    def getBySpecimen(specimenID):
        return DatabaseManager._execute_with_return('SELECT * FROM ResearcherSpecimen WHERE specimenID = ?',
                                                    (specimenID,))
