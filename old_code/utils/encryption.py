# code borrowed from Karen Works, FSU Professor

import base64
from Cryptodome.Cipher import AES


class AESCipher(object):
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, raw):
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        ciphertext = self.cipher.encrypt(raw)
        encoded = base64.b64encode(ciphertext)
        return encoded

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        decrypted = self.cipher.decrypt(decoded)
        return str(decrypted, 'utf-8')


key = b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'
iv = b'OWFJATh1Zowac2xr'

cipher = AESCipher(key, iv)


def encrypt(text):
    return str(cipher.encrypt(bytes(text, 'utf-8')).decode('utf-8'))


def decrypt(text):
    return str(cipher.decrypt(bytes(text, 'utf-8')))
