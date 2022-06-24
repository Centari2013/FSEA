import os.path
import json
from passlib.hash import bcrypt


class userTable:
    def __init__(self):
        self.users = {}

    def loadCredentials(self, filepath):
        if os.path.exists(filepath):
            dataFile = open(filepath, 'r')
            self.users = json.load(dataFile)
            return True
        else:
            return False

    def authenticate(self, user, password):
        if user.lower() in self.users:
            if bcrypt.verify(bytes(password, 'utf-8'), bytes(self.users[user.lower()], 'utf-8')):
                return True
        return False  # wrong pass/ user does not exist

    def addUser(self, user, password):
        # user already exists
        if user.lower() in self.users:
            return False
        # user does not exist
        else:
            self.users[user.lower()] = bcrypt.hash(password)
        return True

    def removeUser(self, user, password):
        if self.authenticate(user, password):
            del self.users[user.lower()]
            return True
        else:
            return False

    def changePassword(self, user, oldPass, newPass):
        if self.authenticate(user, oldPass):
            self.users[user.lower()] = bcrypt.hash(newPass)
            return True
        else:
            return False

    def writeCredentials(self, filepath):
        with open(filepath, 'w+') as dataFile:
            json.dump(self.users, dataFile)

    def clearUserTable(self):
        self.users.clear()
