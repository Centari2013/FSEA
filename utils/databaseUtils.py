import sqlite3
from variables import db
from utils.encryption import encrypt, decrypt
from authUtils import generateUID, generatePWD, generateUsername


def addDepartment(name, supervisor=None, desc=None):
    # encrypt data
    name = encrypt(name)
    if desc is not None:
        desc = encrypt(desc)

    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

        cur = con.cursor()

        cur.execute('INSERT INTO Department(depName, supervisorID, description) VALUES(?,?,?)',
                    (name, supervisor, desc))

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateDepartment(ID, name=None, supervisor=None, desc=None):
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

        args = [[name, 'depName'], [supervisor, 'supervisorID'], [desc, 'description']]

        for a in args:
            if a[0] is not None:
                cur.execute('''UPDATE Department
                                   SET {} = ?
                                   WHERE depID = ?'''.format(a[1]), (a[0], ID))

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
        row = cur.execute('SELECT empID FROM Employee WHERE empID = ?', ID)

        while row is not None:
            ID = generateUID()
            row = cur.execute('SELECT empID FROM Employee WHERE empID = ?', ID)

        cur.execute('''INSERT INTO Employee(empDep, empID, designation, firstName, lastName, startDate) 
                        VALUES(?,?,?,?,?,?)''', (dep, ID, role, fName, lName, sDate))

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

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()
