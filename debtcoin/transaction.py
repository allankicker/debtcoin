from contextlib import contextmanager
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import os, binascii, hashlib, base58, ecdsa
from binascii import hexlify, unhexlify
import codecs


def to_base64(hex_bs):
    decoded = codecs.decode(hex_bs, "hex")
    return codecs.encode(decoded, "base64")

def to_hex(b64_bs):
    decoded = codecs.decode(b64_bs, "base64")
    return codecs.encode(decoded, "hex")

def new_couple_key():
    """
    Return a tuple (priv key, address) as bytes arrays
    """
    sk = ecdsa.SigningKey.from_string(os.urandom(32), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return {
        'priv': to_base64(hexlify(sk.to_string())),
        'pub': to_base64(hexlify(vk.to_string()))
    }


def get_addr(pubkey):
    return to_base64(SHA256.new(pubkey).hexdigest())


def get_pubkey(privkey):
    """
    Return the pub_key from priv_key
    """
    sk = ecdsa.SigningKey.from_string(unhexlify(to_hex(privkey)), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    pub_key = to_base64(binascii.hexlify(vk.to_string()))
    return pub_key


@contextmanager
def open_priv_key(filepath):
    f = open(filepath, 'r')
    key = ECC.importKey(f.read())
    f.close()
    yield key


def sign(transaction, keyfilepath):
    with open_priv_key(keyfilepath) as sender_priv:
        sender_pub = get_pubkey(sender_priv)
        transaction.append(hexlify(sender_pub.to_der()))
        sig = sender_priv.sign(transaction)


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


def check(pubkey, tx_data):
    pass

def sign(sender_privkey_path, tx_data):
    """
    Make transaction script and sign it
    tx_data contain [receiver_addr, amount, tx_id]
    Final transaction script is an ordered list :
    [
        sender_addr,    # len 33 ascii
        receiver_addr,  # len 33 ascii
        amount,         # 16 digits size with padding zeroes, with 2 digits after comma float, ex : 0000000000001.00
        sender_pub,     # sender pub (128 bits ascii)
        tx_id           # 8 digits int
        transaction_sig #
    ]
    sender_addr, sender_pub and transaction_sig are computed from sender_privkey_path
    """
    _check_tx_data(tx_data)
    with open_priv_key(sender_privkey_path) as privkey:
        pubkey = get_pubkey(privkey)
        sender_addr = get_addr(pubkey)
        unsig_script = [
            sender_addr,
            tx_data[0],
            tx_data[1],
            pubkey,
            tx_data[2],
        ]
        unsig_script_b = b"".join(unsig_script)
        sig = privkey.sign(unsig_script_b)
    sig_script = unsig_script + sig
    return sig_script
