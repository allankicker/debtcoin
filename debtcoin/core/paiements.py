from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import os, binascii, hashlib, base58, ecdsa
from binascii import hexlify, unhexlify


def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


def gen_key_addr():
    """
    Return a tuple (priv key, address) as bytes arrays
    """
    # generate private key , uncompressed WIF starts with "5"
    priv_key = os.urandom(32)
    fullkey = binascii.hexlify(priv_key).decode()
    sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
    sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
    WIF = base58.b58encode(binascii.unhexlify(fullkey + sha256b[:8]))

    # get public key , uncompressed address starts with "1"
    sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
    hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
    publ_addr_a = b"\x00" + hash160
    checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
    publ_addr_b = base58.b58encode(publ_addr_a + checksum)
    # Private Key : WIF.decode())
    # Address : publ_addr_b.decode())
    return (WIF, publ_addr_b)


def get_pub_key(priv_key):
    """
    Return the pub_key from priv_key
    """
    sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
    return sk.get_verifying_key()

@contextmanager
def open_priv_key(filepath):
    f = open(filepath, 'r')
    key = ECC.importKey(f.read())
    f.close()
    yield key


def sign(transaction, keyfilepath):
    with openkey(keyfilepath) as sender_priv:
        sender_pub = get_pub_key(sender_priv)
        transaction.append(hexlify(sender_pub.to_der()))
        sig = key.sign(transaction)



def verify(tx_hash, key):
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(tx_hash, key)
        return True
    except ValueError:
        return False


def _check_pub(pub):
    """
    Check the pub key have a valid size
    """
    barr = bytearray(pub, 'ascii')
    if len(pub)



def pay(sender_key_path, receiver_pub, tx_data):
    """
    transaction script (ordered list):
    [
        receiver_pub, #

    ]

    :param sender_key_path: sender priv key filepath
    :param receiver_pub: ECC 256 bits key string
    :param tx_data: {
                        "amount": float (will be truncated to 2 digits after comma
                        "id" : an uuid4 random id (couple id,amount,receiver_pub,sender_pub must be unique)
                    }
    :return:
    """
    hasher = SHA256.new()
    hasher.update()


    pass
