import sqlite3
from random import randint
import secrets
import string
from utils import encryption


def authenticate(user, pwd):
    # TODO add exception handling
    # encrypt username and password for comparison to encrypted database
    user = str(encryption.cipher.encrypt(bytes(user, 'utf-8')).decode('utf-8'))
    pwd = str(encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode('utf-8'))

    # connnect to database
    con = sqlite3.connect('FSEA.db')

    cur = con.cursor()
    cur.execute('select password from Employee where username = ? ', [user])

    # get tuple containing singular password
    p = cur.fetchone()
    if p is not None:
        # convert tuple to list and extract string by indexing
        p = list(p)[0]
        if pwd == p: # user authenticated
            return True
        else:  # password does not match user
            # TODO implement login attempt counter
            return False
    else: # user does not exist
        return False


def generateUID():  # generate random 8 digit str(int)
    uid = randint(0, 99999999)
    uid = str(uid)

    uid = uid.zfill(8)
    return uid


def generatePWD():  # generate random temp password for new users
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(8))
    password = password + '-'
    password += ''.join(secrets.choice(alphabet) for _ in range(8))
    return password
