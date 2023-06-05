import secrets
import sqlite3
import string
from random import randint
from utils.filePaths import DB_PATH
from utils.encryption import encrypt


def authenticate(user, pwd):
    return_val = None
    user = encrypt(user)
    pwd = encrypt(pwd)
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('SELECT password, loginAttempts FROM Credentials WHERE username = ? ;', [user])
        result = cur.fetchone()
        if result is not None:
            p = result[0]
            loginAttempts = result[1]
            if (pwd == p) and loginAttempts < 3:
                if loginAttempts != 0:
                    cur.execute('''UPDATE Credentials
                                    SET loginAttempts = 0
                                    WHERE username = ?''', (user,))
                    con.commit()
                return_val = True
            else:
                if loginAttempts == 3:
                    return_val = "Too many login attempts. Your account is locked."
                else:
                    cur.execute('''UPDATE Credentials
                                    SET loginAttempts = loginAttempts + 1
                                    WHERE username = ?''', (user,))
                    con.commit()
                    return_val = False
        else:
            return_val = False
    except Exception as e:
        print(e)
        return_val = False
    finally:
        if con is not None:
            con.close()
        return return_val


def generateEID():
    uid = str(randint(0, 9999999)).zfill(7)
    return 'E' + uid


def generateSID():
    oid = str(randint(0, 9999999)).zfill(7)
    return 'S' + oid


def generateOID():
    oid = str(randint(0, 9999999)).zfill(7)
    return 'O' + oid


def generateMID():
    mid = str(randint(0, 9999999)).zfill(7)
    return 'M' + mid


def generateUsername(firstName, lastName, dep):
    def firstNLetters(s, n):
        new_s = ""
        if len(s) >= n:
            new_s = s[:n]
        else:
            new_s = s
        return new_s

    username = (firstName[0] + firstNLetters(lastName, 8)).lower() + '_' + str(dep)
    return encrypt(username)


def generatePWD():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(8))
    password = password + '-'
    password += ''.join(secrets.choice(alphabet) for _ in range(8))
    return encrypt(password)
