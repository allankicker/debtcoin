import pytest
from debtcoin import gen_key_addr

@pytest.fixture(scope='session')
def sender_key():

    key = gen_key_addr()


@pytest.fixture(scope='session')
def one_transaction():

    tx_data = [
        sender_addr,  # len 33 ascii
        receiver_addr,  # len 33 ascii
        amount,  # 16 digits size with padding zeroes, with 2 digits after comma float, ex : 0000000000001.00
        sender_pub,  # sender pub (128 bits ascii)
        tx_id  # 8 digits int
        transaction_sig  # ?
    ]



def test_sign():

    pass
