from contextlib import contextmanager
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import os, binascii, ecdsa
from binascii import hexlify, unhexlify
import codecs

ADDR_SIZE = 45
AMOUNT_SIZE = 16
TXID_SIZE = 8
PUB_SIZE = 90

def hex_to_base64(hex_bs):
    decoded = codecs.decode(hex_bs, "hex")
    return codecs.encode(decoded, "base64")


def base64_to_hex(b64_bs):
    decoded = codecs.decode(b64_bs, "base64")
    return codecs.encode(decoded, "hex")


def priv_from_b64(b64_bs):
    return ecdsa.SigningKey.from_string(unhexlify(base64_to_hex(b64_bs)), curve=ecdsa.SECP256k1)


def pub_from_b64(b64_bs):
    return ecdsa.SigningKey.from_string(unhexlify(base64_to_hex(b64_bs)), curve=ecdsa.SECP256k1)


def new_couple_key():
    """
    Return a dict with priv key and pub key as bytes arrays
    """
    sk = ecdsa.SigningKey.from_string(os.urandom(32), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return {
        'priv': hex_to_base64(hexlify(sk.to_string())),
        'pub': hex_to_base64(hexlify(vk.to_string()))
    }


def get_addr(pubkey):
    return hex_to_base64(SHA256.new(pubkey).hexdigest())


def get_pubkey(privkey):
    """
    Return the pub_key from priv_key
    """
    sk = ecdsa.SigningKey.from_string(unhexlify(base64_to_hex(privkey)), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    pub_key = hex_to_base64(binascii.hexlify(vk.to_string()))
    return pub_key


@contextmanager
def open_priv_key(filepath):
    f = open(filepath, 'r')
    key = ECC.importKey(f.read())
    f.close()
    yield key


def sign_with_file(transaction, keyfilepath):
    with open_priv_key(keyfilepath) as sender_priv:
        sender_pub = get_pubkey(sender_priv)
        transaction.append(hexlify(sender_pub.to_der()))
        sig = sender_priv.sign(transaction)

    return sig


def sign(transaction, privkey):
    sk = ecdsa.SigningKey.from_string(priv_from_b64(privkey))
    return sk.sign(transaction)


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
    return b"%016.2f" % (float(value_str))


def _check_tx_data(tx_data):
    sender_addr = tx_data[0]
    receiver_addr = tx_data[1]
    amount = tx_data[2]
    sender_pub = tx_data[3]
    tx_id = tx_data[4]

    if len(tx_data) != 5:
        raise ValueError("tx_data must be a 5 items list")
    if len(sender_addr) != ADDR_SIZE or len(receiver_addr) != ADDR_SIZE :
        raise ValueError("addr must be %s length hex string" % (ADDR_SIZE))
    if len(amount) != AMOUNT_SIZE:
        raise ValueError("amount must be %s length hex string" % (AMOUNT_SIZE))
    try:
        float(amount)
    except ValueError:
        raise ValueError("amount must be a valid float as a string")
    if len(tx_id) != TXID_SIZE:
        raise ValueError("tx_id must be len %s 8 int" % (TXID_SIZE))
    if (len(sender_pub)) != PUB_SIZE:
        raise ValueError("pub keys must be %s length base64 string" % (PUB_SIZE))


def tx_to_string(tx_data):
    return b"".join(tx_data)


def tx_from_string(tx_str):
    return [
        tx_str[:33],
        tx_str[33:66],
        tx_str[66:82],
        tx_str[82:210],
        tx_str[210:218],
    ]
    pass


def check(pubkey, tx_data):
    pass


def sign(privkey, tx_data):
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
        transaction_sig # len 90 
    ]
    sender_addr, sender_pub and transaction_sig are computed from sender_privkey_path
    """
    _check_tx_data(tx_data)
    unsig_script_b = tx_to_string(tx_data)
    sk = priv_from_b64(privkey)
    sig = sk.sign(unsig_script_b)
    tx_data.append(sig)
    return tx_data
