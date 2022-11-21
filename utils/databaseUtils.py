import sqlite3
from variables import db
from utils.encryption import encrypt, decrypt
from authUtils import generateUID, generatePWD, generateUsername


def addDepartment(name, superID=None, desc=None):
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
        updateDepartment(row, superID=superID, desc=desc)




    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateDepartment(ID, name=None, superID=None, desc=None):
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

        args = [[name, 'depName'], [superID, 'supervisorID'], [desc, 'description']]

        for a in args:
            if a[0] is not None:
                cur.execute('''UPDATE Department
                                   SET {} = ?
                                   WHERE depID = ?'''.format(a[1]), (a[0], ID))
        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def deleteDeparment(ID):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        cur.execute('DELETE FROM Department WHERE depID = ?', ID)
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


def updateEmployee(ID, dep=None, role=None, fName=None, lName=None, sDate=None, eDate=None):
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
                                WHERE empID = ?'''.format(a[1]), (a[0], ID))

            con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def deleteEmployee(ID):
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        cur.execute('DELETE FROM Employee WHERE empID = ?', ID)

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateEmployeeMedical(ID, dob=None, btype=None, sex=None, kg=None, h=None, notes=None):
    # encrypt data
    if kg is not None:
        kg = encrypt(str(kg))
    if h is not None:
        h = encrypt(h)
    if notes is not None:
        notes = encrypt(notes)

    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        args = [[dob, 'dob'], [btype, 'bloodtype'], [sex, 'sex'],
                [kg, 'kilograms'], [h, 'height'], [notes, 'notes']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE EmployeeMedical SET {} = ? WHERE empID = ?'.format(a[1]), (a[0], ID))

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateCredentials(ID, uname=None, pwd=None, logAttempts=None):
    # encrypt data
    if uname is not None:
        uname = encrypt(uname)
    if pwd is not None:
        pwd = encrypt(pwd)

    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)
        cur = con.cursor()

        args = [[uname, 'username'], [pwd, 'password'], [logAttempts, 'loginAttempts']]

        for a in args:
            if a[0] is not None:
                cur.execute('UPDATE Credentials SET {} = ? WHERE empID = ?'.format(a[1]), (a[0], ID))

        con.commit()

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()

# TODO: complete helper functions
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

def updateOrigin(ID,
                 name=None, missionID=None, desc=None):
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
            cur.execute('UPDATE Origin SET {} = ? WHERE originID = ?'.format(a[1]), (a[0], ID))

        con.commit()
    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def deleteOrigin(ID):
    con = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('DELETE FROM Origin WHERE originID = ?', ID)
        con.commit()

    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()


def addMission(name, desc, oID=None, sDate=None, eDate=None, capID=None, superID=None):
    # encrypt data
    name = encrypt(name)
    desc = encrypt(desc)

    con = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('INSERT INTO Mission(name, description) VALUES (?,?)', (name, desc))
        con.commit()

        updateMission(cur.lastrowid, name)


def updateMission(ID, name=None, desc=None, oID=None, sDate=None, eDate=None, capID=None, superID=None)
# def deleteMission(ID)
# def addSpecimen(name, oID=None, mID=None, threat=None, dob=None, notes=None)
# def updateSpecimen(ID, name=None, oID=None, mID=None, threat=None, dob=None, notes=None)
# def deleteSpecimen(ID)
# def addEmployeeSpecimen(eID, sID)
# def updateEmployeeSpecimen(eID, sID, newEiD=None, newEiD=None)
# def deleteEmployeeSpecimen(eID, sID)
# def updateSpecimenMedical(ID, btype=None, sex=None, kg=None, notes=None)



