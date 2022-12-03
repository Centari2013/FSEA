import sqlite3
from utils.variables import db
from utils.authUtils import generateUID, generateUsername, generatePWD, generateOID

'''''''''''''''''''''ALTER DATABASE'''''''''''''''''''''


# TODO: ADD USER_FRIENDLY ID RETURNS FROM ALL FUNCTIONS
def addDepartment(name, supervisorID=None, desc=None):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        cur.execute('INSERT INTO Department(depName) VALUES(?)', (name,))
        con.commit()
        row = cur.lastrowid
        updateDepartment(row, supervisorID, desc)

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateDepartment(depID, name=None, supervisorID=None, desc=None):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        args = [[name, 'depName'], [supervisorID, 'supervisorID'], [desc, 'description']]

        for a in args:
            if a[0] is not None:
                cur.execute('''UPDATE Department
                                   SET {} = ?
                                   WHERE depID = ?'''.format(a[1]), (a[0], depID))
        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def deleteDepartment(depID):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        cur.execute('DELETE FROM Department WHERE depID = ?', depID)
        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def addEmployee(firstName, lastName, dep, role, startDate, summary=None):
    ID = None
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        # check for repeat ID
        ID = generateUID()
        cur.execute('SELECT empID FROM Employee WHERE empID = ?', (ID,))
        r1 = cur.fetchone()
        cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', (ID,))
        r2 = cur.fetchone()

        while r1 and r2 is not None:
            ID = generateUID()
            cur.execute('SELECT empID FROM Employee WHERE empID = ?', (ID,))
            r1 = cur.fetchone()
            cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', (ID,))
            r2 = cur.fetchone()

        cur.execute('''INSERT INTO Employee(empDep, empID, designation, firstName, lastName, startDate) 
                        VALUES(?,?,?,?,?,?)''', (dep, ID, role, firstName, lastName, startDate))
        cur.execute('''INSERT INTO EmployeeMedical (empID) VALUES (?)''', (ID,))
        cur.execute('''INSERT INTO Credentials (empID, username, password) 
                        VALUES (?,?,?) ''', (ID, generateUsername(firstName, lastName, role), generatePWD()))
        con.commit()
        updateEmployee(ID, summary=summary)

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return ID


def updateEmployee(empID, dep=None, role=None, firstName=None, lastName=None, startDate=None, endDate=None, summary=None):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        args = [[dep, 'empDep'], [role, 'designation'], [firstName, 'firstName'],
                [lastName, 'lastName'], [startDate, 'startDate'], [endDate, 'endDate'], [summary, 'summary']]

        for a in args:
            if a[0] is not None:
                cur.execute('''UPDATE Employee
                                SET {} = ?
                                WHERE empID = ?'''.format(a[1]), (a[0], empID))

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def deleteEmployee(empID):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        cur.execute('DELETE FROM Employee WHERE empID = ?', (empID,))

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateEmployeeMedical(empID, dob=None, bloodtype=None, sex=None, kg=None, height=None, notes=None):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        args = [[dob, 'dob'], [bloodtype, 'bloodtype'], [sex, 'sex'],
                [kg, 'kilograms'], [height, 'height'], [notes, 'notes']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE EmployeeMedical SET {} = ? WHERE empID = ?'.format(a[1]), (a[0], empID))

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateCredentials(empID, username=None, pwd=None, loginAttempts=None):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)
        cur = con.cursor()

        args = [[username, 'username'], [pwd, 'password'], [loginAttempts, 'loginAttempts']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE Credentials SET {} = ? WHERE empID = ?'.format(a[1]), (a[0], empID))

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def addOrigin(name, desc, missionID=None):
    con = None
    ID = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        oid = generateOID()

        cur.execute('SELECT originID FROM Origin WHERE originID = ?', (oid,))
        r = cur.fetchone()

        while r is not None:
            oid = generateOID()
            cur.execute('SELECT originID FROM Origin WHERE originID = ?', (oid,))
            r = cur.fetchone()

        cur.execute('INSERT INTO Origin(originID, name, description) VALUES (?,?,?)', (oid, name, desc))
        con.commit()
        ID = cur.lastrowid
        updateOrigin(ID, missionID=missionID)
    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
        return ID


def updateOrigin(rowID, name=None, missionID=None, desc=None):
    con = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        args = [[name, 'name'], [missionID, 'missionID'], [desc, 'description']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE Origin SET {} = ? WHERE id = ?'.format(a[1]), (a[0], rowID))

        con.commit()
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def deleteOrigin(originID):
    con = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('DELETE FROM Origin WHERE originID = ?', (originID,))
        con.commit()

    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def addMission(name, desc, originID=None, startDate=None, endDate=None, captainID=None, supervisorID=None):
    ID = None
    con = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        mid = generateOID()

        cur.execute('SELECT originID FROM Origin WHERE originID = ?', (mid,))
        r = cur.fetchone()

        while r is not None:
            mid = generateOID()
            cur.execute('SELECT missionID FROM Mission WHERE missionID = ?', (mid,))
            r = cur.fetchone()

        cur.execute('INSERT INTO Mission(missionID, name, description) VALUES (?,?,?)', (mid, name, desc))
        con.commit()
        ID = cur.lastrowid
        updateMission(ID, name, originID, startDate, endDate, captainID, supervisorID)
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()
        return ID


def updateMission(rowID, name=None, desc=None, originID=None, startDate=None, endDate=None, captainID=None,
                  supervisorID=None):
    con = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        args = [[name, 'name'], [desc, 'description'], [originID, 'originID'], [startDate, 'startDate'],
                [endDate, 'endDate'], [captainID, 'captainID'], [supervisorID, 'supervisorID']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE Mission SET {} = ? WHERE id = ?'.format(a[1]), (a[0], rowID))

        con.commit()
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def deleteMission(missionID):
    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('DELETE FROM Mission WHERE missionID = ?', (missionID,))
        con.commit()

    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def addSpecimen(name, acquisitionDate, originID=None, missionID=None, threatLevel=None, notes=None, description=None):
    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        # check for repeat ID
        ID = generateUID()
        cur.execute('SELECT empID FROM Employee WHERE empID = ?', (ID,))
        r1 = cur.fetchone()
        cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', (ID,))
        r2 = cur.fetchone()

        while r1 and r2 is not None:
            ID = generateUID()
            cur.execute('SELECT empID FROM Employee WHERE empID = ?', (ID,))
            r1 = cur.fetchone()
            cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', (ID,))
            r2 = cur.fetchone()

        cur.execute('INSERT INTO Specimen(specimenID, name, acquisitionDate) VALUES (?,?,?)',
                    (ID, name, acquisitionDate))
        cur.execute('INSERT INTO SpecimenMedical(specimenID) VALUES (?)', (ID,))
        con.commit()

        updateSpecimen(cur.lastrowid, originID, missionID, threatLevel, notes, description)

    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def updateSpecimen(rowID, name=None, acquisitionDate=None, originID=None, missionID=None, threatLevel=None, notes=None, description=None):
    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        args = [[name, 'name'], [acquisitionDate, 'acquisitionDate'], [originID, 'originID'],
                [missionID, 'missionID'], [threatLevel, 'threatLevel'], [notes, 'notes'], [description, 'description']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE Specimen SET {} = ? WHERE id = ?'.format(a[1]), (a[0], rowID))

        con.commit()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def deleteSpecimen(specimenID):
    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('DELETE FROM Specimen WHERE specimenID = ?', (specimenID,))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def addEmployeeSpecimen(empID, specimenID):
    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('INSERT INTO EmployeeSpecimen(empID, specimenID) VALUES(?,?)', (empID, specimenID))
        con.commit()
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def updateSpecimenSupervisor(empID, specimenID, newEmployeeID):
    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('''UPDATE EmployeeSpecimen
                        SET empID = ?
                        WHERE empID = ? AND specimenID = ?''', (newEmployeeID, empID, specimenID))
        con.commit()
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def updateSupervisorSpecimen(empID, specimenID, newSpecimenID):
    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('''UPDATE EmployeeSpecimen
                            SET specimenID = ?
                            WHERE empID = ? AND specimenID = ?''', (newSpecimenID, empID, specimenID))
        con.commit()
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def deleteEmployeeSpecimen(empID, specimenID):
    con = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('DELETE FROM EmployeeSpecimen WHERE empID = ? AND specimenID = ?', (empID, specimenID))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def updateSpecimenMedical(specimenID, name=None, acquisitionDate=None, bloodtype=None, sex=None, kg=None, notes=None):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        args = [[name, 'name'], [acquisitionDate, 'acquisitionDate'], [bloodtype, 'bloodtype'], [sex, 'sex'],
                [kg, 'kilograms'], [notes, 'notes']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE SpecimenMedical SET {} = ? WHERE specimenID = ?'.format(a[1]), (a[0], specimenID))

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
