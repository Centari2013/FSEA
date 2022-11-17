import sqlite3
from utils import encryption


def addEmployee(ID, dep, role, fName, lName, sDate):
    con = None
    try:
        # connect to database
        con = sqlite3.connect('FSEA.db')

        cur = con.cursor()
        cur.execute('''INSERT INTO Employee(empDep, empID, designation, firstName, lastName, startDate) 
                        VALUES(?,?,?,?,?,?)''', (dep, ID, role, fName, lName, sDate))

    except Exception as e:
        print(e)

    finally:
        # close connection and return
        if con is not None:
            con.close()


def updateEmployee(ID, dep=None, role=None, fName=None, lName=None, sDate=None, eDate=None):
    con = None
    try:
        # connect to database
        con = sqlite3.connect('FSEA.db')

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
