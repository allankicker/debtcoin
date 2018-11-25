from contextlib import contextmanager
from Crypto.PublicKey import RSA


@contextmanager
def openkey(filepath):

    f = open(filepath,'r')
    key = RSA.importKey(f.read())
    f.close()
    yield key


def sign(transaction, keyfilepath):

    with openkey(keyfilepath):
        return key.sign(transaction, '')
        

