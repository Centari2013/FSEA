import sqlite3
from random import randint
import secrets
import string
from utils.variables import db
from utils.encryption import encrypt, decrypt


def authenticate(user, pwd):
    return_val = None
    # encrypt username and password for comparison to encrypted database
    user = encrypt(user)
    pwd = encrypt(pwd)
    print(user, user)
    con = None
    try:
        # connect to database
        con = sqlite3.connect(db)

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
    except Exception as e:
        print(e)
        return_val = False
    finally:
        if con is not None:
            con.close()

        return return_val


def generateEID():
    uid = randint(0, 9999999)
    uid = str(uid)

    uid = uid.zfill(7)
    return 'E' + uid

def generateSID():
    oid = randint(0, 9999999)
    oid = str(oid)

    oid = oid.zfill(7)
    return 'S' + oid

def generateOID():
    oid = randint(0, 9999999)
    oid = str(oid)

    oid = oid.zfill(7)
    return 'O' + oid


def generateMID():
    mid = randint(0, 9999999)
    mid = str(mid)

    mid = mid.zfill(7)
    return 'M' + mid


def generateUsername(firstName, lastName, designation):
    def firstNLetters(s, n):
        new_s = ""
        if len(s) >= n:
            for i in range(0, n):
                new_s = new_s + s[i]
        else:
            for i in range(0, len(s)):
                new_s = new_s + s[i]

        return new_s

    username = (firstName[0] + firstNLetters(lastName, 8)).lower() + '_' + designation.upper()

    return encrypt(username)


def generatePWD():  # generate random temp password for new users
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(8))
    password = password + '-'
    password += ''.join(secrets.choice(alphabet) for _ in range(8))
    return encrypt(password)
