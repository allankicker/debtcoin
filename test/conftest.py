import pytest
import ecdsa
from debtcoin.transaction import tx_to_string, pub_from_b64, new_couple_key, sign, hex_to_base64, base64_to_hex, \
    tx_to_string, _format_float
from binascii import hexlify, unhexlify


@pytest.fixture(scope='session')
def alice():
    return {
        'addr': b'0uMKPuenXj2OgwCmkJrBx/0hyBBUfHD62+UjZmcIKMM=\n',
        'priv': b'AQntnDjTY70rtKvGw/2cQg2G/ewZzJDek0nsXX4I74E=\n',
        'pub': b'QmLKOxAYzlb6yqoBjrPSHKUTJD3EIg+O6J4+bQkiQVJEI+222FQiQBbvzih6LcKLsGuYULzSkjmn\nX4DBTg0EKw==\n'
    }


@pytest.fixture(scope='session')
def bob():
    return {
        'addr': b'MhoN1j01RbMnkZv0gORqdWGhXUZm4nxJx7cf5V8DNSQ=\n',
        'priv': b'hOJaDSbzGT9n26L5S2ltE3GLUcybx4MJsMan9Pun7bg=\n',
        'pub': b'eZaTKvnQL4M364ls+P2nAPNEv7rIBxvl4YHKxjzAXsPpC9Cj8zyQ0lMT+QzqqoNZdg+FIkfoD3FP\nwbD7KCoOQA==\n'
    }


@pytest.fixture(scope='session')
def alice_to_bob(alice, bob):
    return [
        alice['addr'],
        bob['addr'],
        b'0000000000010.00',
        alice['pub'],
        b'12345678',
    ]


@pytest.fixture(scope='session')
def bob_to_alice(alice, bob):
    return [
        bob['addr'],
        alice['addr'],
        b'0000000000006.00',
        bob['pub'],
        b'12345678',
    ]
