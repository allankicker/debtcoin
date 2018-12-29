import os
import pytest
from debtcoin.client import cursor, init_table, store, balance
from debtcoin.transaction import  sig_to_base64, priv_from_b64, tx_to_string

TEST_DB_FILE = 'pytest.db'

@pytest.fixture(scope='session')
def cursor_test():
    with cursor(TEST_DB_FILE) as cur:
        init_table(cur)
        yield cur

    os.remove(TEST_DB_FILE)


def test_balance(cursor_test, alice, bob, alice_to_bob, bob_to_alice):

    # store 2 transactions
    # alice pay 10 to bob
    alice_sk = priv_from_b64(alice['priv'])
    sig = sig_to_base64(alice_sk.sign(tx_to_string(alice_to_bob)))
    store(cursor_test, alice_to_bob, sig)

    # bob pay 6 to alice
    bob_sk = priv_from_b64(bob['priv'])
    sig = sig_to_base64(bob_sk.sign(tx_to_string(bob_to_alice)))
    store(cursor_test, bob_to_alice, sig)

    bal = balance(cursor_test, alice['addr'])
    assert bal == -4.0






