import pytest
import ecdsa
from debtcoin.transaction import tx_to_string, pub_from_b64, new_couple_key, sign, hex_to_base64, base64_to_hex, tx_to_string, _format_float
from binascii import hexlify, unhexlify

def test_sign(alice_to_bob, alice):

    sig = sign(alice['priv'], alice_to_bob)
    assert len(sig) == 64
    vk = pub_from_b64(alice['pub'])
    vk.verify(sig, tx_to_string(alice_to_bob))
