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
    #  Private Key : WIF.decode())
    # Address : publ_addr_b.decode())
    return (WIF, publ_addr_b)

def get_addr_from_pubkey(pubkey):


def get_pubkey(privkey):
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
    pass


def _format_float(value_str):
    return "%016.2f" % (float(value_str))


def _check_tx_data(tx_data):
    if len(tx_data) != 3:
        raise ValueError("tx_data must be a 3 items list : [receiver_addr, amount, tx_id]")
    if len(tx_data[0]) != 33:
        raise ValueError("receiver_addr must be 33 length hex string")
    if len(tx_data[1]) != 16:
        raise ValueError("amount must be 16 length hex string")
    try:
        float(tx_data[1])
    except ValueError:
        raise ValueError("amount must be a valid float as a string")
    if len(tx_data[2]) != 8:
        raise ValueError("tx_id must be len 8 int")

def _to_string(tx_data):
    tx_str = ""
    for item in tx_data:
        tx_str += item
    return tx_str

def _from_string(tx_str):
    # TODO
    pass


def pay(sender_privkey_path, tx_data):
    """
    transaction script (ordered list):
    [
        sender_addr,    # len 33 ascii
        receiver_addr,  # len 33 ascii
        amount,         # 16 digits size with padding zeroes, with 2 digits after comma float, ex : 0000000000001.00
        sender_pub,     # sender pub (128 bits ascii)
        tx_id           # 8 digits int
        transaction_sig # ?
    ]

    sender_addr, sender_pub and transaction_sig are deducted from sender_privkey_path
    tx_data contain [receiver_addr, amount, tx_id]
    """
    with open_priv_key(sender_privkey_path) as priv_key:

    hasher = SHA256.new()
    hasher.update()
