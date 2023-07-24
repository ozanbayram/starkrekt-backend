import sqlite3

class Database():
    def __init__(self):
        self.vt = sqlite3.connect('/home/ozan/starkrekt-backend/approve.sqlite')
        self.im = self.vt.cursor()
        self.im.execute("""CREATE TABLE IF NOT EXISTS approve (block_no, tx_hash, tx_from, contract, spender, kind)""") #kind i silecem burdan
        self.im.execute("""CREATE TABLE IF NOT EXISTS contract (contract, name, kind)""")

    def approve_insert_data(self, block_no, tx_hash, tx_from, contract, spender, kind):
        params = (block_no, tx_hash, tx_from, contract, spender, kind)
        self.im.execute("""INSERT INTO approve VALUES (?, ?, ?, ?, ?, ?)""", params)
        self.vt.commit()

    def approve_get_data(self, tx_from):
        params = (hex(tx_from),)
        self.im.execute("""SELECT * FROM approve WHERE tx_from = ? """, params)
        data = self.im.fetchall()
        key = ("block_no", "tx_hash", "tx_from", "contract", "spender", "type")
        datax = list()
        for d in data:
            pair = dict(zip(key, d))
            datax.append(pair)
        return datax
    
    def approve_get_full(self):
        self.im.execute("""SELECT block_no FROM approve""")
        data = self.im.fetchall()
        key = ("block_no", "tx_hash", "tx_from", "contract", "spender", "type")
        datax = list()
        for d in data:
            pair = dict(zip(key, d))
            datax.append(pair)
        return datax
    
    def contract_init(self, contract):
        params = (contract,)
        self.im.execute("""SELECT contract FROM contract WHERE contract = ? """, params)
        if not self.im.fetchone():
            params = (contract, None, None)
            self.im.execute("""INSERT INTO contract VALUES (?, ?, ?)""", params)
            self.vt.commit()

    def contract_update_name(self, contract ,name):
        params = (name, contract)
        self.im.execute("""UPDATE contract SET name = ? WHERE contract = ? """, params)
        self.vt.commit()

    def contract_get_name(self, contract):
        params = (contract,)
        self.im.execute("""SELECT name FROM contract WHERE contract = ? """, params)
        data = self.im.fetchone()
        if data:
            return data[0]
        return None
 
    def contract_update_kind(self, contract, kind):
        params = (kind, contract)
        self.im.execute("""UPDATE contract SET kind = ? WHERE contract = ? """, params)
        self.vt.commit()

    def contract_get_kind(self, contract):
        params = (contract,)
        self.im.execute("""SELECT kind FROM contract WHERE contract = ? """, params)
        data = self.im.fetchone()
        if data:
            return data[0]
        return None
    
    def delete(self):
        self.im.execute("""ALTER TABLE approve DROP type""")
        self.vt.commit()

if __name__ == "__main__":   
    db=Database()
    w=db.approve_get_full()
    #a=(db("0x00da114221cb8355fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3))
    #print(a)
    print(w)






