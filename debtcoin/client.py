import sqlite3
from contextlib import contextmanager
from debtcoin.transaction import check_tx_data

TABLE = ''' 
        CREATE TABLE IF NOT EXISTS tx 
        (senderaddr BLOB check(length(senderaddr) == 33), 
        receiveraddr CHARACTER(33) check(length(receivderaddr) == 33), 
        amount FLOAT check(amount > 0), 
        senderpub CHARACHTER(128) check(length(senderpub) == 128), 
        txid SMALLINT,
        UNIQUE(senderaddr, receiveraddr, amount, txid)
        sig CHARACTER(90) check(length(sig) == 90)) 
        '''

@contextmanager
def cursor():
    conn = sqlite3.connect('transactions.db')
    curs = conn.cursor()
    yield curs
    conn.commit()
    conn.close()

def init_table(curs):
    curs.execute(TABLE)


def store(tx_data):
    check_tx_data(tx_data)
    db_data = (
        tx_data[0],
        tx_data[1],
        float(tx_data[2]),
        tx_data[3],
        int(tx_data[4]),
        tx_data[5],
    )
    with cursor() as cur:
        cur.execute('INSERT INTO tx VALUES(?,?,?,?,?,?)', [db_data])




