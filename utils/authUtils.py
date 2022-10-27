import sqlite3
from random import randint
import secrets
import string
from utils import encryption


def authenticate(user, pwd):
    return_val = None
    # encrypt username and password for comparison to encrypted database
    user = str(encryption.cipher.encrypt(bytes(user, 'utf-8')).decode('utf-8'))
    pwd = str(encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode('utf-8'))

    try:
        # connnect to database
        con = sqlite3.connect('FSEA.db')

        cur = con.cursor()
        cur.execute('SELECT password FROM Credentials WHERE username = ? ;', [user])

        # get tuple containing singular password
        p = cur.fetchone()
        if p is not None:
            # convert tuple to list and extract string by indexing
            p = list(p)[0]
            if pwd == p:  # user authenticated
                return_val = True
            else:  # password does not match user
                cur.execute('''UPDATE Credentials
                                SET loginAttempts = loginAttempts + 1
                                WHERE username = ?''', [user])
                return_val = False
        else:  # user does not exist
            return_val = False
    except:
        print('Error connecting to FSEA database')
        return_val = False

    # close connection and return
    con.close()
    return return_val


def generateUID():  # generate random 8 digit str(int)
    uid = randint(0, 99999999)
    uid = str(uid)

    uid = uid.zfill(8)
    return uid


def generateUsername(empID):
    def firstNLetters(s, n):
        new_s = ""
        if len(s) >= n:
            for i in range(0, n):
                new_s = new_s + s[i]
        else:
            for i in range(0, len(s)):
                new_s = new_s + s[i]

        return new_s

    try:
        con = sqlite3.connect('FSEA.db')
        cur = con.cursor()
        cur.execute('''SELECT firstName, lastName, designation 
                        FROM Employee
                        WHERE empID = ?;''', [empID])
        query = cur.fetchone()
        if query is not None:
            query = list(query)
            firstName = str(encryption.cipher.decrypt(bytes(query[0], 'utf-8')).encode('utf-8').decode('utf-8'))
            lastName = str(encryption.cipher.decrypt(bytes(query[1], 'utf-8')).encode('utf-8').decode('utf-8'))
            designation = query[2]

            username = (firstName[0] + firstNLetters(lastName, 8)).lower() + '_' + designation.upper()
            username = str(encryption.cipher.encrypt(bytes(username, 'utf-8')).decode('utf-8'))

            return username

    except:
        print('Could not access database.')

    return None


def generatePWD():  # generate random temp password for new users
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(8))
    password = password + '-'
    password += ''.join(secrets.choice(alphabet) for _ in range(8))
    return password
