import sqlite3

class Database():
    def __init__(self):
        self.vt = sqlite3.connect('/app/approve.sqlite')
        self.im = self.vt.cursor()
        self.im.execute("""CREATE TABLE IF NOT EXISTS approve (
                            tx_from TEXT, 
                            contract TEXT, 
                            spender TEXT,
                            UNIQUE(tx_from, contract, spender))""")
        
        self.im.execute("CREATE INDEX IF NOT EXISTS idx_approve_tx_from ON approve(tx_from)")

        self.im.execute("""CREATE TABLE IF NOT EXISTS contract (
                            contract TEXT, 
                            name TEXT, 
                            kind TEXT)""")

    def approve_insert_data(self, tx_from, contract, spender):
        params = (tx_from, contract, spender)
        try:
            self.im.execute("""INSERT INTO approve(tx_from, contract, spender) 
                               VALUES (?, ?, ?)""", params)
            self.vt.commit()
        except sqlite3.IntegrityError:
            print("Record already exists and won't be added again.")

    def approve_get_data(self, tx_from):
        params = (tx_from,)
        self.im.execute("""SELECT * FROM approve WHERE tx_from = ? """, params)
        data = self.im.fetchall()
        key = ("tx_from", "contract", "spender")
        datax = [dict(zip(key, d)) for d in data]
        return datax
    
    def approve_get_full(self):
        self.im.execute("""SELECT * FROM approve""")
        data = self.im.fetchall()
        key = ("tx_from", "contract", "spender")
        datax = [dict(zip(key, d)) for d in data]
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
    
if __name__ == "__main__":   
    db=Database()
    #w=db.approve_get_full()
    #a=(db("0x00da114221cb8355fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3))
    #print(a)
    #print(w[-1])
    k=db.contract_get_kind("0x50031010bcee2f43575b3afe197878e064e1a03c12f2ff437f29a2710e0b6ef")
    print(k)






