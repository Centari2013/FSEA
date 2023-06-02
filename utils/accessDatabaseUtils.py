import sqlite3
from utils.filePaths import DB_PATH




def getDepartmentData(depID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT * FROM Department WHERE depID = ?', (depID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getSpecimenContainmentStatusData(specimenID) -> list:
    # TODO: test
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = lambda cursor, row: row[0]  # returns ids as list
        cur = con.cursor()
        cur.execute('SELECT statusID FROM SpecimenContainmentStatus WHERE specimenID = ?', (specimenID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getContainmentStatusData(statusID) -> list:
    # TODO: test
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = lambda cursor, row: row[0]  # returns ids as list
        cur = con.cursor()
        cur.execute('SELECT * FROM ContainmentStatus WHERE statusID = ?', (statusID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getDepartmentMissionData(depID) -> list:
    # TODO: test
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = lambda cursor, row: row[0]  # returns ids as list
        cur = con.cursor()
        cur.execute('SELECT missionID FROM DepartmentMission WHERE depID = ?', (depID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getEmployeeMissionData(empID) -> list:
    # TODO: test
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = lambda cursor, row: row[0]  # returns ids as list
        cur = con.cursor()
        cur.execute('SELECT missionID FROM EmployeeMission WHERE empID = ?', (empID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getSpecimenMissionData(specimenID) -> list:
    # TODO: test
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = lambda cursor, row: row[0]  # returns ids as list
        cur = con.cursor()
        cur.execute('SELECT missionID FROM SpecimenMission WHERE specimenID = ?', (specimenID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getEmployeeDesignationData(empID) -> list:
    # TODO: test
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = lambda cursor, row: row[0]  # returns ids as list
        cur = con.cursor()
        cur.execute('SELECT designationID FROM EmployeeDesignation WHERE empID = ?', (empID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getDesignationData(designationID) -> list:
    # TODO: test
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = lambda cursor, row: row[0]  # returns ids as list
        cur = con.cursor()
        cur.execute('SELECT * FROM Designation WHERE designationID = ?', (designationID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getEmployeeData(empID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute('''SELECT * FROM Employee WHERE empID = ?''', (empID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getEmployeeClearanceData(empID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = lambda cursor, row: row[0]  # returns ids as list
        cur = con.cursor()

        cur.execute('''SELECT clearanceID FROM EmployeeClearance WHERE empID = ?''', (empID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getClearanceData(clearanceID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute('''SELECT * FROM Clearance WHERE clearanceID = ?''', (clearanceID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getEmployeeMedicalData(empID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT * FROM EmployeeMedical WHERE empID = ?', (empID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getOriginData(originID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT * FROM Origin WHERE originID = ?', (originID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getMissionData(missionID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT * FROM Mission WHERE missionID = ?', (missionID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getSpecimenData(specimenID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT * FROM Specimen WHERE specimenID = ?', (specimenID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getSpecimenMedicalData(specimenID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT * FROM SpecimenMedical WHERE specimenID = ?', (specimenID,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getSpecimenEmployees(specimenID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT empID FROM EmployeeSpecimen WHERE specimenID = ?', (specimenID,))
        data = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data


def getEmployeeSpecimens(empID):
    con = None
    data = None
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT specimenID FROM EmployeeSpecimen WHERE empID = ?', (empID,))
        data = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return data
