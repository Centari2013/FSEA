import sqlite3
from utils.filePaths import DB_PATH
from utils.authUtils import generateEID, generateUsername, generatePWD, generateOID, generateMID, generateSID
from utils.encryption import encrypt
import traceback

'''''''''''''''''''''ALTER DATABASE'''''''''''''''''''''


def print_sql(sql):
    print("Last executed SQL query: ", sql)
    return str



def addContainmentStatus(name, desc):
    ID = None
    con = None

    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('INSERT INTO ContainmentStatus(name, description) VALUES(?,?);', (name, desc))
        con.commit()
        row = cur.lastrowid
        cur.execute('SELECT containmentStatusID FROM ContainmentStatus WHERE rowid = ?', (row,))
        ID = cur.fetchone()[0]

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        if ID is not None:
            return ID


def updateContainmentStatus(containmentStatusID, name=None, desc=None):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[name, 'name'], [desc, 'desc']]
        for a in args:
            if a[0] is not None:
                cur.execute(f'''UPDATE ContainmentStatus SET {a[1]} = ? WHERE containmentStatusID = ?''', (a[0], containmentStatusID))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def deleteContainmentStatus(containmentStatusID):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM ContainmentStatus WHERE containmentStatusID = ?', (containmentStatusID,))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success

















def addClearance(name, desc):
    ID = None
    con = None

    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('INSERT INTO Clearance(name, description) VALUES(?,?);', (name, desc))
        con.commit()
        row = cur.lastrowid
        cur.execute('SELECT clearanceID FROM Clearance WHERE rowid = ?', (row,))
        ID = cur.fetchone()[0]

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        if ID is not None:
            return ID


def updateClearance(clearanceID, name=None, desc=None):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[name, 'name'], [desc, 'desc']]
        for a in args:
            if a[0] is not None:
                cur.execute(f'''UPDATE Clearance SET {a[1]} = ? WHERE clearanceID = ?''', (a[0], clearanceID))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def deleteClearance(clearanceID):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM Clearance WHERE clearanceID = ?', (clearanceID,))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def addEmployeeClearance(empID, cleranceID):
    ID = None
    con = None

    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('INSERT INTO EmployeeClearance(empID, clearanceID) VALUES(?,?);', (empID, cleranceID))
        con.commit()
        row = cur.lastrowid
        cur.execute('SELECT empID, clearanceID FROM EmployeeClearance WHERE rowid = ?', (row,))
        ID = cur.fetchone()[0]

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        if ID is not None:
            return ID


def updateEmployeeClearance(empID, clearanceID, newClearanceID):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute(f'''UPDATE EmployeeClearance SET clearanceID = ? WHERE empID = ? AND clearanceID = ?''',
                    (empID, clearanceID, newClearanceID))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def deleteEmployeeClearance(empID, clearanceID):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM EmployeeClearance WHERE empID = ? AND clearanceID = ?', (empID, clearanceID,))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def addDesignation(name, abbreviation):
    ID = None
    con = None

    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('INSERT INTO Designation(name, abbreviation) VALUES(?,?);', (name, abbreviation))
        con.commit()
        row = cur.lastrowid
        cur.execute('SELECT designationID FROM Designation WHERE rowid = ?', (row,))
        ID = cur.fetchone()[0]

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        if ID is not None:
            return ID


def updateDesignation(designationID, name=None, abbreviation=None):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[name, 'name'], [abbreviation, 'abbreviation']]
        for a in args:
            if a[0] is not None:
                cur.execute(f'''UPDATE Designation SET {a[1]} = ? WHERE designationID = ?''', (a[0], designationID))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def deleteDesignation(designationID):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM Designation WHERE designationID = ?', (designationID,))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def addDepartment(name, supervisorID=None, desc=None):
    ID = None
    con = None

    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('INSERT INTO Department(depName) VALUES(?);', (name,))
        con.commit()
        row = cur.lastrowid
        cur.execute('SELECT depID FROM Department WHERE rowid = ?', (row,))
        ID = cur.fetchone()[0]
        updateDepartment(ID, supervisorID=supervisorID, desc=desc)

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        if ID is not None:
            return ID


def updateDepartment(depID, name=None, supervisorID=None, desc=None):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[name, 'depName'], [supervisorID, 'supervisorID'], [desc, 'description']]
        for a in args:
            if a[0] is not None:
                cur.execute(f'''UPDATE Department SET {a[1]} = ? WHERE depID = ?''', (a[0], depID))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def deleteDepartment(depID):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM Department WHERE depID = ?', (depID,))
        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def addEmployee(firstName, lastName, dep, startDate, summary=None):
    ID = None
    con = None
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        # check for repeat ID
        ID = generateEID()
        cur.execute('SELECT empID FROM Employee WHERE empID = ?', (ID,))
        r1 = cur.fetchone()
        cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', (ID,))
        r2 = cur.fetchone()

        while r1 and r2 is not None:
            ID = generateEID()
            cur.execute('SELECT empID FROM Employee WHERE empID = ?', (ID,))
            r1 = cur.fetchone()
            cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', (ID,))
            r2 = cur.fetchone()

        cur.execute('''INSERT INTO Employee(empDep, empID,firstName, lastName, startDate) 
                        VALUES(?,?,?,?,?)''', (dep, ID, firstName, lastName, startDate))
        con.commit()

        updateEmployee(ID, summary=summary)
        updateCredentials(ID, username=generateUsername(firstName, lastName, dep), pwd=generatePWD())

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return ID


def addEmployeeDesignation(empID, designationID):
    ID = None
    con = None
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('''INSERT INTO EmployeeDesignation(empID, designationID) 
                        VALUES(?,?)''', (empID, designationID))
        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return ID


def updateEmployee(empID, dep=None, role=None, firstName=None, lastName=None, startDate=None, endDate=None,
                   summary=None):
    con = None
    success = False

    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[dep, 'empDep'], [role, 'designation'], [firstName, 'firstName'],
                [lastName, 'lastName'], [startDate, 'startDate'], [endDate, 'endDate'], [summary, 'summary']]

        for a in args:
            if a[0] is not None:
                cur.execute('''UPDATE Employee
                                SET {} = ?
                                WHERE empID = ?'''.format(a[1]), (a[0], empID))

        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def deleteEmployee(empID):
    con = None
    success = False

    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM Employee WHERE empID = ?', (empID,))

        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def updateEmployeeMedical(empID, dob=None, bloodtype=None, sex=None, kg=None, height=None, notes=None):
    con = None
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)

        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[dob, 'dob'], [bloodtype, 'bloodtype'], [sex, 'sex'],
                [kg, 'kilograms'], [height, 'height'], [notes, 'notes']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE EmployeeMedical SET {} = ? WHERE empID = ?'.format(a[1]), (a[0], empID))

        con.commit()
        success = True

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def updateCredentials(empID, username=None, pwd=None, loginAttempts=None):
    con = None
    username = encrypt(username)
    pwd = encrypt(pwd)
    success = False
    try:
        # connect to database
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[username, 'username'], [pwd, 'password'], [loginAttempts, 'loginAttempts']]

        for a in args:
            if a[0] is not None:
                cur.execute(f'UPDATE Credentials SET {a[1]} = ? WHERE empID = ?', (a[0], empID))

        con.commit()
        success = True

    except Exception as e:
        print(e)
        traceback.print_exc()

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return success


def addOrigin(name, desc, missionID=None):
    con = None
    ID = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        ID = generateOID()

        cur.execute('SELECT originID FROM Origin WHERE originID = ?', (ID,))
        r = cur.fetchone()

        while r is not None:
            ID = generateOID()
            cur.execute('SELECT originID FROM Origin WHERE originID = ?', (ID,))
            r = cur.fetchone()

        cur.execute('INSERT INTO Origin(originID, name, description) VALUES (?,?,?)', (ID, name, desc))
        con.commit()

        updateOrigin(ID, missionID=missionID)
    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return ID


def updateOrigin(ID, name=None, missionID=None, desc=None):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        args = [[name, 'name'], [missionID, 'missionID'], [desc, 'description']]

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

        cur.execute('SELECT missionID FROM Origin WHERE missionID = ?', (ID,))
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


def addEmployeeSpecimen(empID, specimenID):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('INSERT INTO EmployeeSpecimen(empID, specimenID) VALUES(?,?)', (empID, specimenID))
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

        cur.execute('''UPDATE EmployeeSpecimen
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

        cur.execute('''UPDATE EmployeeSpecimen
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


def deleteEmployeeSpecimen(empID, specimenID):
    con = None
    success = False
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute('DELETE FROM EmployeeSpecimen WHERE empID = ? AND specimenID = ?', (empID, specimenID))
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
