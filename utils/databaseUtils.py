import sqlite3
from variables import db
from utils.encryption import encrypt, decrypt
from authUtils import generateUID, generatePWD, generateUsername


def addDepartment(name, supervisorID=None, desc=None):
    # encrypt data
    name = encrypt(name)
    if desc is not None:
        desc = encrypt(desc)

    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        cur.execute('INSERT INTO Department(depName) VALUES(?)',
                    name)
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
    # encrypt data
    if name is not None:
        name = encrypt(name)
    if desc is not None:
        desc = encrypt(desc)

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


def addEmployee(fName, lName, dep, role, sDate):
    fName = encrypt(fName)
    lName = encrypt(lName)

    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        # check for repeat empID
        ID = generateUID()
        cur.execute('SELECT empID FROM Employee WHERE empID = ?', ID)
        r1 = cur.fetchone()
        cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', ID)
        r2 = cur.fetchone()

        while r1 and r2 is not None:
            ID = generateUID()
            cur.execute('SELECT empID FROM Employee WHERE empID = ?', ID)
            r1 = cur.fetchone()
            cur.execute('SELECT specimenID FROM Specimen WHERE specimenID = ?', ID)
            r2 = cur.fetchone()

        cur.execute('''INSERT INTO Employee(empDep, empID, designation, firstName, lastName, startDate) 
                        VALUES(?,?,?,?,?,?)''', (dep, ID, role, fName, lName, sDate))

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateEmployee(empID, dep=None, role=None, fName=None, lName=None, sDate=None, eDate=None):
    # encrypt data
    if fName is not None:
        fName = encrypt(fName)
    if lName is not None:
        lName = encrypt(lName)

    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        args = [[dep, 'empDep'], [role, 'designation'], [fName, 'firstName'],
                [lName, 'lastName'], [sDate, 'startDate'], [eDate, 'endDate']]

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

        cur.execute('DELETE FROM Employee WHERE empID = ?', empID)

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateEmployeeMedical(empID, dob=None, bloodtype=None, sex=None, kg=None, height=None, notes=None):
    # encrypt data
    if kg is not None:
        kg = encrypt(str(kg))
    if height is not None:
        height = encrypt(height)
    if notes is not None:
        notes = encrypt(notes)

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
    # encrypt data
    if username is not None:
        username = encrypt(username)
    if pwd is not None:
        pwd = encrypt(pwd)

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
    # encrypt data
    name = encrypt(name)
    desc = encrypt(desc)

    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('INSERT INTO Origin(name, description) VALUES (?,?)', (name, desc))
        con.commit()
        updateOrigin(cur.lastrowid, missionID)
    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateOrigin(rowID, name=None, missionID=None, desc=None):
    # encrypt data
    if name is not None:
        name = encrypt(name)
    if desc is not None:
        desc = encrypt(desc)

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

        cur.execute('DELETE FROM Origin WHERE originID = ?', originID)
        con.commit()

    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def addMission(name, desc, originID=None, startDate=None, endDate=None, captainID=None, supervisorID=None):
    # encrypt data
    name = encrypt(name)
    desc = encrypt(desc)

    con = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('INSERT INTO Mission(name, description) VALUES (?,?)', (name, desc))
        con.commit()

        updateMission(cur.lastrowid, name, originID, startDate, endDate, captainID, supervisorID)
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def updateMission(rowID, name=None, desc=None, originID=None, startDate=None, endDate=None, captainID=None,
                  supervisorID=None):
    # encrypt data
    if name is not None:
        name = encrypt(name)
    if desc is not None:
        desc = encrypt(desc)

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

        cur.execute('DELETE FROM Mission WHERE missionID = ?', missionID)
        con.commit()

    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def addSpecimen(name, acquisitionDate, originID=None, missionID=None, threatLevel=None, notes=None):
    # encrypt data
    name = encrypt(name)
    if notes is not None:
        notes = encrypt(notes)

    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('INSERT INTO Specimen(name, acquisitionDate) VALUES (?,?)', (name, acquisitionDate))
        con.commit()

        updateSpecimen(cur.lastrowid, originID, missionID, threatLevel, notes)

    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def updateSpecimen(rowID, name=None, acquisitionDate=None, originID=None, missionID=None, threatLevel=None, notes=None):
    # encrypt data
    if name is not None:
        name = encrypt(name)
    if notes is not None:
        notes = encrypt(notes)

    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        args = [[name, 'name'], [acquisitionDate, 'acquisitionDate'], [originID, 'originID'],
                [missionID, 'missionID'], [threatLevel, 'threatLevel'], [notes, 'notes']]

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

        cur.execute('DELETE FROM Specimen WHERE specimenID = ?', specimenID)
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
    # encrypt data
    if kg is not None:
        kg = encrypt(str(kg))
    if notes is not None:
        notes = encrypt(notes)

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
