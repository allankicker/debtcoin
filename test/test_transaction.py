import pytest
import ecdsa
from debtcoin.transaction import new_couple_key, sign, hex_to_base64, base64_to_hex, tx_to_string, _format_float
from binascii import hexlify, unhexlify


@pytest.fixture(scope='session')
def receiver():
    return {
        'addr': b'0uMKPuenXj2OgwCmkJrBx/0hyBBUfHD62+UjZmcIKMM=\n',
        'priv': b'AQntnDjTY70rtKvGw/2cQg2G/ewZzJDek0nsXX4I74E=\n',
        'pub': b'QmLKOxAYzlb6yqoBjrPSHKUTJD3EIg+O6J4+bQkiQVJEI+222FQiQBbvzih6LcKLsGuYULzSkjmn\nX4DBTg0EKw==\n'
    }

@pytest.fixture(scope='session')
def sender():
    return {
        'addr': b'MhoN1j01RbMnkZv0gORqdWGhXUZm4nxJx7cf5V8DNSQ=\n',
        'priv': b'hOJaDSbzGT9n26L5S2ltE3GLUcybx4MJsMan9Pun7bg=\n',
        'pub': b'eZaTKvnQL4M364ls+P2nAPNEv7rIBxvl4YHKxjzAXsPpC9Cj8zyQ0lMT+QzqqoNZdg+FIkfoD3FP\nwbD7KCoOQA==\n'
    }



@pytest.fixture(scope='session')
def tx_data(sender, receiver):

    return [
        sender['addr'],  # len 33 ascii
        receiver['addr'],  # len 33 ascii
        b'0000000000010.00',  # 16 digits size with padding zeroes, with 2 digits after comma float,
        sender['pub'],  # sender pub (128 bits ascii)
        b'12345678',  # 8 digits int
    ]



def test_sign(tx_data, sender):

    sig_script = sign(sender['priv'], tx_data)
    print(hex_to_base64(hexlify(sig_script[5])))

