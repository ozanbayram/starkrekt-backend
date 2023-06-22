import sqlite3

class Database():
    def __init__(self):
        self.vt = sqlite3.connect('/home/ozan/starkrevoke/approve.sqlite')
        self.im = self.vt.cursor()
        self.im.execute("""CREATE TABLE IF NOT EXISTS approve (block_no, tx_hash, tx_from, contract, spender, kind)""")

    def insert_data(self, block_no, tx_hash, tx_from, contract, spender, kind):
        params = (block_no, tx_hash, tx_from, contract, spender, kind)
        self.im.execute("""INSERT INTO approve VALUES (?, ?, ?, ?, ?, ?)""", params)
        self.vt.commit()

    def get_data(self, tx_from):
        params = (hex(tx_from),)
        self.im.execute("""SELECT * FROM approve WHERE tx_from = ? """, params)
        data = self.im.fetchall()
        key = ("block_no", "tx_hash", "tx_from", "contract", "spender", "type")
        datax = list()
        for d in data:
            pair = dict(zip(key, d))
            datax.append(pair)
        return datax
    
    def get_full(self):
        self.im.execute("""SELECT block_no FROM approve""")
        data = self.im.fetchall()
        key = ("block_no", "tx_hash", "tx_from", "contract", "spender", "type")
        datax = list()
        for d in data:
            pair = dict(zip(key, d))
            datax.append(pair)
        return datax
    
if __name__ == "__main__":   
    db=Database()
    print(len(db.get_full()))





