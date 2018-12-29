import sqlite3
from contextlib import contextmanager
from debtcoin.transaction import check_sig

TABLE_CREATE_QUERY = ''' 
        CREATE TABLE IF NOT EXISTS tx 
        (senderaddr BLOB check(length(senderaddr) == 45), 
        receiveraddr BLOB check(length(receiveraddr) == 45), 
        amount FLOAT check(amount > 0), 
        senderpub BLOB check(length(senderpub) == 90), 
        txid SMALLINT,
        sig BLOB check(length(sig) == 90),
        UNIQUE(senderaddr, receiveraddr, amount, txid))
        '''

INPUTS_QUERY = '''select sum(amount) from tx where receiveraddr = ?'''
OUTPUTS_QUERY = '''select sum(amount) from tx where senderaddr = ?'''


@contextmanager
def cursor(db_file='transactions.db'):
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    yield curs
    conn.commit()
    conn.close()


def init_table(curs):
    curs.execute(TABLE_CREATE_QUERY)


def store(curs, tx_data, sig):
    check_sig(tx_data, sig)
    db_data = (
        tx_data[0],
        tx_data[1],
        float(tx_data[2]),
        tx_data[3],
        int(tx_data[4]),
        sig,
    )
    curs.execute('INSERT INTO tx VALUES(?,?,?,?,?,?)', db_data)


def balance(curs, addr):
    inputs = curs.execute(INPUTS_QUERY, (addr,)).fetchone()[0]
    outputs = curs.execute(OUTPUTS_QUERY, (addr,)).fetchone()[0]
    return inputs - outputs
